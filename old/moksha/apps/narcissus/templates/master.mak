<html>
<head>
<title>Narcissus -- Realtime usage from http://mirror.rit.edu/</title>
<style type="text/css">
/*TOOLTIPS*/
.tip {
    color: #111;
    width: 139px;
    background-color: white;
    border:1px solid #ccc;
    -moz-box-shadow:#555 2px 2px 8px;
    -webkit-box-shadow:#555 2px 2px 8px;
    -o-box-shadow:#555 2px 2px 8px;
    box-shadow:#555 2px 2px 8px;
    opacity:0.9;
    filter:alpha(opacity=90);
    font-size:10px;
    font-family:Verdana, Geneva, Arial, Helvetica, sans-serif;
    padding:7px;
}
</style>

</head>
<body>
${tmpl_context.menu_widget.display()}
${self.body()}
</body>
${tmpl_context.moksha_socket.display()}
</html>
