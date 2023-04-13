"""
自定义一个分页组件,以后如果想要使用这个分页组件,你需要做如下几件事情:
def prettynum_list(request):
    # 1.根据自己的情况去筛选自己的数据
    user_list = UserInfo.objects.all()
    # 2.实例化分页对象
    user_queryset = Pagination(request, queryset=user_list)

    context = {
        "user_list": user_queryset.page_queryset,
        "page_str_list": user_queryset.html(),  # 页码
        }
    return render(request, 'user_list.html', context)

在HTML页面中
        {% for obj in list_queryset %}
        <th>{{ obj.id }} </th>
        <th>{{ obj.xxx }} </th>
        {% endfor %}

        <ul class="pagination">
             {{ page_str_list }}
        </ul>

"""
import math
from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据(根据这个数据给他进行分页处理)
        :param page_size:每页显示多少条数据
        :param page_param:在URL中发传递的获取分页的参数 ,例如:/list/?page=12
        :param plus:显示当前页的 前或后几页(页码)
        """
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.begin_n = (self.page - 1) * page_size  # 计算出每页的页数切片值然后放到下面中
        self.end_n = self.page * page_size

        self.page_queryset = queryset[self.begin_n:self.end_n]

        self.total_page_count = queryset.count()

        self.max_page = math.ceil(self.total_page_count / self.page_size)

        self.plus = plus

        self.page_param = page_param

    def html(self):
        # 页码
        page_str_list = []
        self.query_dict.setlist(self.page_param, [1])
        # 首页
        ele = '<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(ele)

        # 上一页
        self.query_dict.setlist(self.page_param, [self.page - 1])
        if self.page > 1:
            ele = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
        ele = '<li ><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(ele)

        # 页面:页面要求1.如果总页码小于等于两倍plus也就是10,那就直接显示全部页码,如果大于两倍plus就显示当前页的前plus页和后plus页 所以设置plus=5

        # 如果数据的总页数小于等于10,直接显示出来1--10,起始值为1,最大值为总页数的max_page
        if self.max_page <= self.plus * 2:
            # 这里设置plus*2是为了默认固定显示10页面作为显示,如果最大页面没有10,那就全部显示,如果有大于10页面,那就要进一步判断
            self.start_page = 1
            self.end_page = self.max_page + 1
        else:  # 上面是总页数小于10全部显示,那下面开始就是总页数大于10的(这里要注意需求要求默认展示10页,故还需要判断当前页和plus的关系)
               # 当前页小于等于5,那就是直接展示10页
            if self.page <= self.plus:  # 这里判断当:前页码是多少,如果是小于plus 5,那就直接显示全部出来(全部为十个页数范围内的数据)
                self.start_page = 1  # 那第一页就是1,要不然直接用当前页page-5,当page小于等于5就会变成0/负值
                self.end_page = self.plus * 2 + 1  # 那最大值就是显示当前10页,10页后的使用page-plus和+plus即可显示前五页和后五页
            else:  # 这里判断:就是当前页大于plus5的数据,那就要要判断最大值
                if (self.page + self.plus) < self.max_page:
                    # 这里判断:当前页+plus后是否小于等于总页数mas_page,小于就显示当前页的前五和后五,大于则要考虑最大值,避免突出页码
                    self.start_page = self.page - self.plus
                    self.end_page = self.page + self.plus + 1
                else:
                    # 这里的判断就是当前页+plus5 等于总页数的,那就是倒推显示,最小值就应该是max_page-2plus,end最大值
                    self.start_page = self.max_page - self.plus * 2
                    self.end_page = self.max_page + 1
        for i in range(self.start_page, self.end_page):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
            # page_str_list = mark_safe("".join(page_str_list)) 不能这么写 AttributeError: 'SafeString' object has no attribute 'append'
            # 证明这个字符串是安全的,以便在前端页面展示

        # 下一页
        if self.page < self.max_page:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            ele = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.max_page])
            ele = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(ele)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.max_page])
        ele = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(ele)

        search_string = """
           <li>
              <form style="float: right" method="get">
                  <input type="text" name="page" class="form-control"
                         style="position: relative;float: left;display: inline-block;width: 180px;border-radius: 10;"
                         placeholder="请输入要跳转至的页面数">
                  <button class="btn btn-default" type="submit">跳转</button>
              </form>
           </li>
           """
        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))
        return page_string
