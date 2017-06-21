#!/usr/bin/env python
# encoding: utf-8

#######################################
#  Requirement:                       #
#  $ sudo pip install wordpress-json  #
#######################################

from wordpress_json import WordpressJsonWrapper

# wp = WordpressJsonWrapper('http://new.hackingthursday.org/wordpress/?rest_route=/wp/v2/posts', '', '')
wp = WordpressJsonWrapper('http://new.hackingthursday.org/wordpress/index.php/wp-json/wp/v2', '', '')

posts = wp.get_posts()
print posts[0].keys()
print posts[0].get('title')
print posts[0].get('author')
