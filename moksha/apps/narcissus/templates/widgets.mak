<%inherit file="moksha.apps.narcissus.templates.master"/>
% for widget in tmpl_context.widgets:
${widget.display() | n}
% endfor
