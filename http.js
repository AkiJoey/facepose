const http = require('http')

const html = `
	<div id="board"></div>

	<script>    
		var frag = document.createDocumentFragment();    
		for (var row = 0;row < 8;row++) {
			for (var col = 0;col < 8;col++) {
				if ((col + row) % 2 != 0) {
					var div =  document.createElement('div');
					div.setAttribute('class', 'cell');
					div.style.top = (row * 50) + 'px';
					div.style.left = (col * 50) + 'px';
					frag.appendChild(div);
				} 
			}
		}
		document.getElementById("board").appendChild(frag);
	</script>

	<style>
		#board {
			width: 400px;
			height: 400px;
			background: #fff;
			border: 1px solid;
			position: relative;
		}
		.cell{
			width: 50px;
			height: 50px;
			background: #000;
			position: absolute;
			top: 0;
			left: 0;
		}
	</style>
`

http.createServer((request, response) => {
	response.end(html)
}).listen(8000, () => {
	console.log('Server running at http://127.0.0.1:8000/')
})
