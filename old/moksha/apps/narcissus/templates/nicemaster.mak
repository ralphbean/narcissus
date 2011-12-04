<html>
<head>
<title>Narcissus -- Realtime usage from http://mirror.rit.edu/</title>
	<!--  I know this is awful.  Sorry. -->
	<style type="text/css">
		#content-container {
				width:100%;
				height:100%;
				align:center;
		}
		#content {
			width: 700px;
			margin:0 auto;
		}
	</style>
</head>
<body>
${tmpl_context.menu_widget.display()}
<div id="content-container">
<div id="content">
${self.body()}
</div>
</div>
</body>
${tmpl_context.moksha_socket.display()}
</html>
