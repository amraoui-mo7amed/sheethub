from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pathlib import Path
import polib
import json
from decouple import config
from mistralai import Mistral
from typing import Dict, List
import os
from tqdm import tqdm
import time

class Command(BaseCommand):
    help = 'Translate .po files using MistralAI for a specific target language'

    def __init__(self):
        super().__init__()
        self.batch_size = 10  # Smaller batch size for reliability
        self.rate_limit_delay = 2  # Delay between API calls in seconds
        self.translation_cache = {}

    def add_arguments(self, parser):
        parser.add_argument(
            '--target-lang',
            type=str,
            required=True,
            choices=[code for code, name in settings.LANGUAGES if code != settings.LANGUAGE_CODE],
            help='Target language code (e.g., ar, fr)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be translated without making changes',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Translate all strings, including already translated ones',
        )

    def handle(self, *args, **options):
        try:
            target_lang = options['target_lang']
            
            # Validate target language
            if target_lang == settings.LANGUAGE_CODE:
                raise CommandError(f"Cannot translate to default language ({settings.LANGUAGE_CODE})")
            
            if target_lang not in dict(settings.LANGUAGES):
                raise CommandError(f"Language {target_lang} not configured in settings.LANGUAGES")

            # Get locale path
            locale_path = getattr(settings, 'LOCALE_PATHS', [None])[0]
            if not locale_path:
                raise CommandError("LOCALE_PATHS not configured in settings")

            # Initialize MistralAI client
            api_key = config('MISTRAL_API_KEY')
            if not api_key:
                raise CommandError("MISTRAL_API_KEY not found in environment variables")
            
            client = Mistral(api_key=api_key)

            # Process target language
            target_name = dict(settings.LANGUAGES)[target_lang]
            self.stdout.write(self.style.SUCCESS(
                f"\nTranslating from {settings.LANGUAGE_CODE} to {target_lang} ({target_name})"
            ))

            # Find all .po files for target language
            target_path = Path(locale_path) / target_lang / 'LC_MESSAGES'
            if not target_path.exists():
                raise CommandError(f"No locale directory found for {target_lang}")

            po_files = list(target_path.glob('*.po'))
            if not po_files:
                raise CommandError(f"No .po files found for {target_lang}")

            # Process each .po file
            for po_file in po_files:
                self.translate_po_file(
                    po_file=po_file,
                    client=client,
                    target_lang=target_lang,
                    dry_run=options['dry_run'],
                    force=options['force']
                )

        except Exception as e:
            raise CommandError(f"Error during translation: {str(e)}")

    def translate_batch(self, client: Mistral, entries: List, target_lang: str) -> Dict:
        """Translate a batch of entries together"""
        # Create a list of texts to translate
        texts_to_translate = []
        for entry in entries:
            # Check cache first
            if entry.msgid in self.translation_cache:
                continue
            texts_to_translate.append(entry.msgid)

        if not texts_to_translate:
            return self.translation_cache

        messages = [
            {
                "role": "system",
                "content": f"Translate these texts to {target_lang}. Return a JSON object with 'translations' as an array of translated texts in the same order. Preserve any HTML tags."
            },
            {
                "role": "user",
                "content": json.dumps(texts_to_translate)
            }
        ]

        try:
            response = client.chat.complete(
                model="mistral-large-latest",
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            content = json.loads(response.choices[0].message.content)
            translations = content.get('translations', [])
            
            # Update cache with new translations
            for original, translated in zip(texts_to_translate, translations):
                self.translation_cache[original] = translated
            
            return self.translation_cache

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Batch translation error: {str(e)}"))
            return self.translation_cache

    def translate_po_file(self, po_file: Path, client: Mistral, target_lang: str, dry_run: bool, force: bool):
        """Translate a single .po file"""
        self.stdout.write(f"\nProcessing {po_file.name}...")
        
        po = polib.pofile(str(po_file))
        entries_to_translate = [entry for entry in po if force or not entry.msgstr]

        if not entries_to_translate:
            self.stdout.write(self.style.SUCCESS("All entries already translated"))
            return

        # Group entries into small batches
        batches = [
            entries_to_translate[i:i + self.batch_size] 
            for i in range(0, len(entries_to_translate), self.batch_size)
        ]

        with tqdm(total=len(entries_to_translate), desc="Translating") as pbar:
            for batch in batches:
                max_retries = 3
                retry_count = 0
                
                while retry_count < max_retries:
                    try:
                        # Maintain consistent rate limit delay
                        time.sleep(self.rate_limit_delay)
                        translations = self.translate_batch(client, batch, target_lang)
                        
                        if not dry_run:
                            for entry in batch:
                                if entry.msgid in translations:
                                    entry.msgstr = translations[entry.msgid]
                        
                        pbar.update(len(batch))
                        break
                    
                    except Exception as e:
                        retry_count += 1
                        if "429" in str(e):  # Rate limit
                            wait_time = 60  # Full minute wait on rate limit
                            self.stdout.write(self.style.WARNING(
                                f"Rate limit reached, waiting {wait_time} seconds..."
                            ))
                            time.sleep(wait_time)
                        else:
                            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
                            time.sleep(5)  # General error delay

        if not dry_run:
            # Save translations
            po.save()
            # Compile .mo file
            mo_file = po_file.with_suffix('.mo')
            po.save_as_mofile(str(mo_file))
            
            self.stdout.write(self.style.SUCCESS(
                f"Translated {len(entries_to_translate)} strings in {po_file.name}"
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Would translate {len(entries_to_translate)} strings in {po_file.name} (dry run)"
            ))