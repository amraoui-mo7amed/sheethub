let revenueChartInstance = null;
let ordersChartInstance = null;
let topProductsChartInstance = null;

document.addEventListener('DOMContentLoaded', function () {
    const userNameDiv = document.querySelector(".user-name");

    if (!userNameDiv) return; // safety check

    const userRole = userNameDiv.dataset.userRole; // read data attribute

    if (userRole === "admin") {
        (() => {
            const wrapper = document.querySelector('.row[data-chart-labels]');
            if (!wrapper) return;

            // Raw data
            const labels = wrapper.dataset.chartLabels.split(',');
            const sellers = wrapper.dataset.chartSellers.split(',').map(Number);
            const deliveries = wrapper.dataset.chartDeliveries.split(',').map(Number);
            const orders = wrapper.dataset.chartOrders.split(',').map(Number);
            const prodLabels = wrapper.dataset.chartProductsLabels.split(',');
            const prodValues = wrapper.dataset.chartProductsValues.split(',').map(Number);

            // Translated titles from data-*
            const titleSellers = wrapper.dataset.titleSellers;
            const titleDeliveries = wrapper.dataset.titleDeliveries;
            const titleOrders = wrapper.dataset.titleOrders;
            const titleProducts = wrapper.dataset.titleProducts;

            const colors = ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796'];

            // Helpers
            const mkLine = (id, data, label, color) =>
                new Chart(document.getElementById(id), {
                    type: 'line',
                    data: { labels, datasets: [{ label, data, fill: false, borderColor: color, tension: 0.3 }] },
                    options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
                });

            const mkBar = (id, data, label, color) =>
                new Chart(document.getElementById(id), {
                    type: 'bar',
                    data: { labels, datasets: [{ label, data, backgroundColor: color }] },
                    options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
                });

            const mkDoughnut = (id, labels, data, label) =>
                new Chart(document.getElementById(id), {
                    type: 'doughnut',
                    data: { labels, datasets: [{ label, data, backgroundColor: colors }] },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }
                });

            // Render
            mkLine('sellersChart', sellers, titleSellers, '#4e73df');
            mkBar('deliveriesChart', deliveries, titleDeliveries, '#1cc88a');
            mkLine('ordersChart', orders, titleOrders, '#f6c23e');
            mkDoughnut('productsChart', prodLabels, prodValues, titleProducts);
        })();
    } else if (userRole === "seller") {
        // Dynamic charts for seller
        fetch("/dashboard/seller-data/")
            .then((response) => {
                if (!response.ok) throw new Error("Network error");
                return response.json();
            })
            .then((data) => {
                // === REVENUE CHART ===
                const revenueCanvas = document.getElementById("revenueChart");
                if (revenueCanvas) {
                    const revenueCtx = revenueCanvas.getContext("2d");
                    if (revenueChartInstance) {
                        revenueChartInstance.destroy();
                        revenueChartInstance = null;
                    }
                    revenueChartInstance = new Chart(revenueCtx, {
                        type: "bar",
                        data: {
                            labels: data.labels,
                            datasets: [
                                {
                                    label: "Total Revenue",
                                    data: data.revenue,
                                    backgroundColor: "rgba(54, 162, 235, 0.6)",
                                },
                                {
                                    label: "Confirmed Revenue",
                                    data: data.status_revenue_per_day.confirmed,
                                    backgroundColor: "rgba(40, 167, 69, 0.6)", // green
                                },
                                {
                                    label: "Shipped Revenue",
                                    data: data.status_revenue_per_day.shipped,
                                    backgroundColor: "rgba(23, 162, 184, 0.6)", // blue
                                },
                                {
                                    label: "Cancelled Revenue",
                                    data: data.status_revenue_per_day.cancelled,
                                    backgroundColor: "rgba(220, 53, 69, 0.6)", // red
                                }
                            ]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    position: 'left',
                                }
                            },
                            plugins: {
                                legend: {
                                    position: 'bottom',
                                    align: 'start' // bottom left
                                }
                            }
                        }
                    });
                }

                // === ORDERS CHART ===
                const ordersCanvas = document.getElementById("ordersChart");
                if (ordersCanvas) {
                    const ordersCtx = ordersCanvas.getContext("2d");
                    if (ordersChartInstance) {
                        ordersChartInstance.destroy();
                        ordersChartInstance = null;
                    }
                    ordersChartInstance = new Chart(ordersCtx, {
                        type: "line",
                        data: {
                            labels: data.labels,
                            datasets: [{
                                label: "Orders",
                                data: data.orders,
                                fill: true,
                                backgroundColor: "rgba(255, 206, 86, 0.3)",
                                borderColor: "rgba(255, 206, 86, 1)",
                                tension: 0.3
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                }

                // === TOP PRODUCTS CHART ===
                const topProductsCanvas = document.getElementById("topProductsChart");
                if (topProductsCanvas) {
                    const topProductsCtx = topProductsCanvas.getContext("2d");
                    if (topProductsChartInstance) {
                        topProductsChartInstance.destroy();
                        topProductsChartInstance = null;
                    }
                    topProductsChartInstance = new Chart(topProductsCtx, {
                        type: "doughnut",
                        data: {
                            labels: data.top_products_labels,
                            datasets: [{
                                label: "Sales",
                                data: data.top_products_values,
                                backgroundColor: [
                                    "#4e73df",
                                    "#1cc88a",
                                    "#36b9cc",
                                    "#f6c23e",
                                    "#e74a3b",
                                    "#858796"
                                ],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            cutout: "0%", // smaller value = thicker ring
                            radius: "100%", // makes the chart fill the canvas
                            plugins: {
                                legend: {
                                    position: 'right',
                                    align: 'start',
                                }
                            }
                        }
                    });
                }
            })
            .catch((error) => {
                console.error("Failed to fetch analytics:", error);
            });
    }

});
