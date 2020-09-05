
let incidentAction = undefined;

testItem = {
    init: function(options) {
        let incidents_container = $('#incidents-list-js');
        let tests_container = $('#tests-list-js');
        let test_item_log_model = $('#modal1');

        function download_incidents(url) {
            $.get(url, function (data) {
                incidents_container.html(data);
                $('#incidents-list-js [data-modal-target]').click(function(){
                    incidentAction = $(this).data('action');
                });
                $.HSCore.components.HSModalWindow.init('#incidents-list-js [data-modal-target]', {
                    'onOpen': function () {
                        $.get(incidentAction, function (data) {
                            test_item_log_model.find('.test-logs-list-js').html(data);
                        });
                    }
                });
            });
        }

        function download_test_results(url) {
            $.get(url, function (data) {
                tests_container.html(data);
                // test_item_log_model.html(data);
            });
        }

        function download_incident_results(url) {
            $.get(url, function (data) {
                test_item_log_model.find('.test-logs-list-js').html(data);
            });
        }

        // initial download
        download_incidents(options.incident_list_url);
        download_test_results(options.test_item_result_list_url);

        // pagination of incidents
        incidents_container.on("click", ".pagination-js a", function(e) {
            e.preventDefault();
            let url2 = options.incident_list_url + $(this).attr('href')
            download_incidents(url2);
        });
        // pagination of test items
        tests_container.on("click", ".pagination-js a", function(e) {
            e.preventDefault();
            let url2 = options.test_item_result_list_url + $(this).attr('href')
            download_test_results(url2);
        });
        // pagination of test items inside incident pop-up
        test_item_log_model.on("click", ".pagination-js a", function(e) {
            e.preventDefault();
            let url2 = options.test_item_result_list_url + $(this).attr('href')
            download_incident_results(url2);
        });

        let = chartColors = {
            red: 'rgb(255, 99, 132)',
            orange: 'rgb(255, 159, 64)',
            yellow: 'rgb(255, 205, 86)',
            green: 'rgb(75, 192, 192)',
            blue: 'rgb(54, 162, 235)',
            purple: 'rgb(153, 102, 255)',
            grey: 'rgb(201, 203, 207)'
        };

		var config = {
			type: 'line',
			data: {
				labels: options.chart.labels,
				datasets: [{
					label: 'Response Time',
                    fill: true,
					backgroundColor: chartColors.red,
					borderColor: chartColors.red,
					data: options.chart.data,
				}]
			},
			options: {
				responsive: true,
				scales: {
					xAxes: [{
						display: true
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'SEC'
						}
					}]
				}
			}
		};

		window.onload = function() {
			var ctx = document.getElementById('canvas').getContext('2d');
			window.myLine = new Chart(ctx, config);
		};

    }

};
