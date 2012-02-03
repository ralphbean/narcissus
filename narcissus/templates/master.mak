<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
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
