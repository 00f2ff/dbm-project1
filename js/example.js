d3.csv('../csv/2003.csv', function(d) {
	return {
		data: d
	};
}, function(error, rows) {
	console.log(rows);
});