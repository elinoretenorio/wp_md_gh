import os
import os.path
import mysql.connector
import html2markdown
import time

# GH username
gh_user = ''
# GH personal access token
gh_token = ''
# without the .git
gh_repo = 'example.com'
# domain to archive
domain = 'example.com'

db = mysql.connector.connect(
    user='', 
    password='',
    host='',
    port=3306,
    database=''
)

ts = time.gmtime()
date_time = time.strftime("%Y-%m-%d %H:%M:%S", ts)

cursor = db.cursor()
query = ("SELECT post_name, post_title, post_date, post_content, post_type FROM wp_posts WHERE post_status = 'publish' ORDER BY post_date ASC;")
cursor.execute(query)

main = open('README.md', 'w')
main.write("### {} archive \n\n".format(domain))

for (post_name, post_title, post_date, post_content, post_type) in cursor:
  html = html2markdown.convert(post_content)
  if not os.path.isdir('{}'.format(post_type)):
    os.mkdir('{}'.format(post_type))

  file = open('{}/{:%Y-%m-%d}-{}.md'.format(post_type, post_date, post_name), 'w')
  file.write("### {}\n\n{:%b %d, %Y}\n\n".format(post_title, post_date))
  file.write(html)
  file.close()

  link = 'https://github.com/{}/{}/blob/main/{}/{:%Y-%m-%d}-{}.md'.format(gh_user, gh_repo, post_type, post_date, post_name)
  main.write("* [{}]({}) {:%Y-%m-%d}\n".format(post_title, link, post_date))

main.close()
cursor.close()
db.close()

path = os.path.dirname(os.path.abspath(__file__))
is_git_dir = os.path.isdir('{}/.git'.format(path))

# git init only if it doesn't exist
if (is_git_dir == False):
    os.system('git init')

# ignore current script
ignore = open('.gitignore', 'w')
ignore.write(__file__)
ignore.close()

# commit to github
os.system('git add .')
os.system('git commit -m "{} commit"'.format(date_time))

# git branch and add remote only if it doesn't exist
if (is_git_dir == False):
    os.system('git branch -M main')
    os.system('git remote add origin https://{}:{}@github.com/{}/{}.git'.format(gh_user, gh_token, gh_user, gh_repo))

# push to github
os.system('git push -u origin main')