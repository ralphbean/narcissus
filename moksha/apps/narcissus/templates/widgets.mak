<%inherit file="moksha.apps.narcissus.templates.master"/>
<div style="margin-left:40px; z-index:-10;">
% for widget in tmpl_context.widgets:
${widget.display() | n}
% endfor
</div>
