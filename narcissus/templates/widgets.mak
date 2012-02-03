<%inherit file="narcissus.templates.master"/>
<div style="z-index:-10;">
% for widget in tmpl_context.widgets:
${widget.display() | n}
% endfor
</div>
