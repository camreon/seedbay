from django.conf.urls import patterns, include, url

urlpatterns = patterns('swap.views',
    url(r'^$', 'home'),
    url(r'^search$', 'search'),
    url(r'^search/results/(?P<query>\S+)$', 'searchResults'),
    url(r'^guide$', 'guide'),
    url(r'^about$', 'about'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),     
    url(r'^register$', 'register'),
    url(r'^my/profile$', 'profile'),
    url(r'^farmers/(?P<requested_user_id>\d+)/seeds/$', 'userSeeds'),
    url(r'^seeds/(?P<requested_seed_id>\d+)/$', 'seedInfo'),
    url(r'^add/item$', 'add_item'),
    url(r'^add/seedtype$', 'add_seedtype'),
)
