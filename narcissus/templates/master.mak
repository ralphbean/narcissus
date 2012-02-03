<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
    <title>Narcissus</title>
  </head>
  <body>
    ${tmpl_context.menu_widget.display() |n }
    ${self.body()}
  </body>
  ${tmpl_context.moksha_socket.display() |n }
</html>
