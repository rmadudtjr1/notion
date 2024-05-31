from django import template
from ..models import Notion

register = template.Library()

@register.inclusion_tag('notion_tree.html')
def render_notion_tree(notion):
    children = notion.children.all()

    if children:  # 자식 노드가 있는 경우에만 재귀 호출 수행
        return {'notion': notion, 'children': children}
    else:  # 자식 노드가 없는 경우에는 빈 딕셔너리 반환
        return {}