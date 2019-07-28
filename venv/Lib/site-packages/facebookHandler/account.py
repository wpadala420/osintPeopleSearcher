from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from .utils import getStringBetween

import time
import random



class Account:

	def __init__(self, CHROMEDRIVER_PATH=None, headless=True):
		options = Options()
		options.headless = headless
		self.browser = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
		self.authenticated = False
		self.id = None
		self.email = None
		self.password = None


	
	def authenticate(self, email, password):
		"""authenticate and store the account id"""
		try:
			self.browser.get("https://m.facebook.com")
			self.browser.find_element_by_name("email").send_keys(email)
			self.browser.find_element_by_name("pass").send_keys(password + Keys.RETURN)

			if  "https://m.facebook.com" == self.browser.current_url:
				raise Exception("wrong email or password")
			self.email = email
			self.password = password
			self.authenticated = True
			time.sleep(5)
			try:		
				self.browser.get("https://m.facebook.com/profile.php")
				elem = self.browser.find_element_by_css_selector('a[href*="/allactivity"]')
				self.id = elem.get_attribute("href").split("/")[-2]
			except:
				raise Exception("cannot get account id")
		except Exception as e:
			print(f"Authentication Failed: {e}")
			self.exit()


	def post_profile(self, text):
		"""make a profile post and return its id"""
		try:
			if not self.authenticated:
				raise(Exception("not authenticated"))
			self.browser.get("https://m.facebook.com/")
			time.sleep(2)
			self.browser.find_element_by_xpath('//div[@role="textbox"]').click()
			textbox = WebDriverWait(self.browser, 10).until(lambda browser: browser.find_element_by_tag_name('textarea'))
			time.sleep(3)
			textbox = self.browser.find_element_by_tag_name('textarea')
			textbox.send_keys(text)
			time.sleep(3)
			textbox.submit()

			time.sleep(5)
	
			posts = self.browser.find_elements_by_css_selector('article')
			if len(posts) == 0:
				raise Exception
			for post in posts:
				toParse = post.get_attribute("data-store")

				# data-store format:{"linkdata":"top_level_post_id.326230754879551:content_owner_id_new.100031212201704:story_location.6","feedback_target":326230754879551,"feedback_source":0,"action_source":0,"actor_id":100031212201704}
				# what we want: 326230754879551 and 100031212201704

				postID = getStringBetween(toParse, "top_level_post_id.", ":content_owner_id_new")
				userID = getStringBetween(toParse, ":content_owner_id_new.", ":story_location")
					
				if userID == self.id:
					return postID 

			raise Exception("cannot find post id")

		except Exception as e:
			print(f"Profile Post Failed: {e}")

	
	def post_group(self, group_id, text):
		"""make a post in a group and return the post id"""
		try:
			if not self.authenticated:
				raise(Exception("not authenticated"))
			self.browser.get(f"https://m.facebook.com/groups/{group_id}")
			self.browser.find_element_by_xpath('//div[@role="textbox"]').click()	 
			textbox = self.browser.find_element_by_tag_name('textarea')
			textbox.send_keys(text)

			time.sleep(10)

			self.browser.find_element_by_css_selector('button[data-sigil="touchable submit_composer"]').click()

			time.sleep(5)
			
			posts = self.browser.find_elements_by_css_selector('article')
			if len(posts) == 0:
				raise Exception("could not find any posts")

			for post in posts:
				toParse = post.get_attribute("data-store")

				# data-store format:{"linkdata":"top_level_post_id.326230754879551:content_owner_id_new.100031212201704:story_location.6","feedback_target":326230754879551,"feedback_source":0,"action_source":0,"actor_id":100031212201704}
				# what we want: 326230754879551 and 100031212201704

				postID = getStringBetween(toParse, "top_level_post_id.", ":content_owner_id_new")
				userID = getStringBetween(toParse, ":content_owner_id_new.", ":story_location")
					
				if userID == self.id:
					return postID 

			raise Exception("cannot find post id")

		except Exception as e:
			print(f"Group Post Failed: {e}")

	
	def accept_all_friends(self):
		"""accept all friend requests"""
		try:
			if not self.authenticated:
				raise(Exception("not authenticated"))

			while True:
				self.browser.get("https://m.facebook.com/friends/center/requests/")
				requests = self.browser.find_elements_by_css_selector('button[value="Confirm"][type="submit"]')
				
				if len(requests) == 0:
					break				

				try:
					for request in requests:
							waitingTime = random.uniform(0.5, 1)		
							time.sleep(waitingTime)
							request.click()

				except Exception:				
					pass

		except Exception as e:
			print(f"Accepting Friend requests failed: {e}")

	
	def get_post_IDs_from_group(self, group_id, depth=0):
		"""returns a list of the first post ids on a group"""
		try:
			if not self.authenticated:
				raise Exception("not authenticated")
			
			self.browser.get(f"https://m.facebook.com/groups/{group_id}")
			time.sleep(1)
			old_height = self.browser.execute_script("return document.body.scrollHeight")
			cur = 0

			while cur < depth:
				self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(6)
				new_height = self.browser.execute_script("return document.body.scrollHeight")
				if new_height == old_height:
					break
				old_height = new_height
				cur += 1

			posts = self.browser.find_elements_by_css_selector('article[data-dedupekey]')

			IDs = []

			for post in posts:

				data = post.get_attribute("data-store")
				#data-store="{"linkdata":"qid.6637150604128350091:mf_story_key.554359628364431:top_level_post_id.554359628364431:tl_objid.554359628364431:content_owner_id_new.100015062925511:text_formatting.518948401838663:src.22:story_location.6","feedback_target":554359628364431,"feedback_source":2,"action_source":0,"actor_id":100031212201704}"
				#what we want: 554359628364431
				postID = getStringBetween(data, "story_key.", ":top_level")
				IDs.append(postID)
			print(f"extracted {len(IDs)} posts from group {group_id}")
			return IDs
		except Exception as e:
			print(f"Getting IDs from group {group_id} failed: {e}")			

	
	def get_comments_from_profile_post(self, post_id):
		"""returns a list of comments on a group post"""
		try:
			if not self.authenticated:
				raise(Exception("not authenticated"))
			self.browser.get(f"https://m.facebook.com/{post_id}")
			comments = self.browser.find_elements_by_css_selector('div[data-commentid]')
			
			extracted = []	

			for comment in comments:
				extracted.append(comment.text)		
							
			print(f"{len(extracted)} comments extracted from profile post: {post_id}")
	
			return extracted

		except Exception as e:
			print(f"extracting comments failed: {e}")


	def get_comments_from_group_post(self, group_id, post_id):
		"""returns a list of comments on a group post"""
		try:
			if not self.authenticated:
				raise(Exception)
			self.browser.get(f"https://m.facebook.com/groups/{group_id}/permalink/{post_id}" )

			waited = False
			while True:
				#<a href="/groups/86093688.." data-sigil="ajaxify">
				previousComments = self.browser.find_elements_by_css_selector('a[data-sigil="ajaxify"]')
				if len(previousComments) == 0:
					break
				else:
					try:
						previousComments[0].click()
						waited = False
						time.sleep(1.5)
					except Exception:
						if waited:
							break
						else:
							time.sleep(1.5)
							waited = True		

			#<div data-commentid="111331716583901_111455283238211" data-sigil="comment-body">ds</div>
			comments = self.browser.find_elements_by_css_selector('div[data-commentid]')
			extracted = []	

			for comment in comments:
				extracted.append(comment.text)						
			print(f"{len(extracted)} comments extracted from group post:{post_id}")
			return extracted		

		except Exception as e:
			print(f"Extracting comments from group post failed: {e}")


	def get_groups(self):
		""" returns a list of groups that the user is currently in """
		try:
			if not self.authenticated:
				raise(Exception("not authenticated"))
			self.browser.get("https://m.facebook.com/groups/?category=groups")
			groups = self.browser.find_elements_by_css_selector('a[href*="/groups/"][aria-labelledby]')

			extracted = []
			for group in groups:
				uid = group.get_attribute("href").split("/")[4].split("?")[0]
				extracted.append(uid)
			print(f"{len(extracted)} groups are found")
			return extracted

		except Exception as e:
			print(f"Getting groups failed: {e}")

	
	def get_most_recent_conversations(self, depth=0):
		""" returns a list of IDs of the nth users that the account had converstations with """
		try:
			if not self.authenticated:
					raise Exception("not authenticated")
			self.browser.get("https://m.facebook.com/messages/")
			cur = 0
			conversations = []	

			while cur < depth:
				try:
					see_more = self.browser.find_element_by_css_selector('div[id="see_older_threads"] > a')
					see_more.click()
					cur += 1
					time.sleep(3)
				except:
					break
			
			
			#id="threadlist_row_other_user_fbid_100002156320758"
			conversations = self.browser.find_elements_by_css_selector('div[id*="threadlist_row_other_user_fbid"]')

			
			infos = []	
			for convo in conversations:
				href = convo.get_attribute("id")
				extracted = href.split("_")[-1]
				infos.append(extracted)			

			return infos

		except Exception as e:
			print(f"Getting convos failed: {e}")

	
	def get_chatlog(self, user_id, depth=0):
		"""returns a list of dictionaries that has data of the last messages the account had
		with the user with user_id"""
		try:
			if not self.authenticated:
				raise Exception("not authenticated")
			self.browser.get(f"https://m.facebook.com/messages/read/?tid={user_id}")	
			time.sleep(5)
			cur_page = 0		
			while cur_page < depth:
				try:
					button = self.browser.find_element_by_css_selector('div[id="see_older"] > a')
					button.click()
					time.sleep(3)
					cur_page += 1
				except:
					print("all convos have loaded")
					break
			

			#<div data-store="{"timestamp":1545136889326,"author":100027122867499,"uuid":"mid.$cAAAAAzX--8Nt8psl7lnwVXceaiFi"}
			infos = self.browser.find_elements_by_css_selector('div[data-store*="timestamp"]')
			messages = []
			#images = []
			for info in infos:
				try:
					messages.append(info.find_element_by_css_selector('span').text)
				except:
					messages.append('')
			#	try:
			#		images.append(info.find_element_by_css_selector('img').get_attribute("src"))
			#	except:
			#		images.append('')

			messages_parsed = []
			
			for i in range(len(infos)):
				data = infos[i].get_attribute("data-store")
				timestamp = getStringBetween(data, '"timestamp":', ',"author"')
				author = getStringBetween(data, '"author":', ',"uuid"')
				content = messages[i]
				#image = images[i]
				if content == '':
					continue
				messages_parsed.append({"author":author, "timestamp":timestamp, "content":content})

			return messages_parsed

		except Exception as e:
			print(f"Getting chatlogs for {user_id} failed: {e}")


	def send_message(self, user_id, message):
		"""send a message to a user"""
		try:
			if not self.authenticated:
				raise Exception("not authenticated")
			if not user_id in self.browser.current_url: 
				self.browser.get(f"https://m.facebook.com/messages/read/?tid={user_id}")	
				time.sleep(5)	
			
			textarea = self.browser.find_element_by_css_selector('textarea')
			textarea.send_keys(message)
			time.sleep(3)

			self.browser.find_element_by_css_selector('button[value="Send"]').click()
	
		except Exception as e:
			print(f"Sending message failed:{e}")


	def send_friend_request(self, user_id):
		"""Send a friend request to a user or reply to an existing friend request"""
		try:
			if not self.authenticated:
				raise Exception("not authenticated")
			self.browser.get(f"https://m.facebook.com/{user_id}")
			try:
				button = self.browser.find_element_by_css_selector('a[role="button"][href*="/a/mobile/friends/profile_add_friend.php?"]')
				button.click()
			except:
				raise Exception(f"you are already friends with user {user_id}")
		except Exception as e:
			print(f"Sending friend request failed: {e}")


	def make_group_comment(self, group_id, post_id, comment_text):
		"""make a comment on a post in a group"""
		try:
			if not self.authenticated:
				raise Exception("not authenticated")
			self.browser.get(f"https://m.facebook.com/groups/{group_id}?view=permalink&id={post_id}")
			self.browser.find_element_by_css_selector('textarea[id="composerInput"]').send_keys(comment_text)
			time.sleep(2)
			button = self.browser.find_element_by_css_selector('button[type=submit][value="Post"]')
			button.click()

		except Exception as e:
			print(f"Making comment on the post {post_id} in {group_id} Failed: {e}")


	def exit(self):
		"""terminate the bot and the webdrive executable"""
		self.browser.quit()