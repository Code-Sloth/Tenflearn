from django import template

register = template.Library()

@register.filter
def divide_by_five(value):
    return value / 5 * 100

def category_kr(value):
    if value == 'all':
        return '전체'
    elif value == 'qna':
        return '질문 & 답변'
    elif value == 'worry':
        return '고민있어요'
    elif value == 'study':
        return '스터디'
    else:
        return '기타'
    
def mypage_kr(value):
    if value == 'course':
        return '내 학습'
    elif value == 'review':
        return '내 수강평'
    else:
        return '수강바구니'    

register.filter('category_kr', category_kr)
register.filter('mypage_kr', mypage_kr)