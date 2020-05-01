##### pip install requests==2.22.0

# _*_ coding:utf-8 _*_

import os
import time
import requests
import json


class DownloadUnsplash(object):
	def __init__(self, photo_name):
		self.num_photo = 1
		self.photo_name = photo_name
		self.start_url = "https://unsplash.com/napi/search/photos?query=" + photo_name + "&xp=&per_page=20&page={}"
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}

	def create_dir(self, directory):
		create_path = r"./Unsplash/{}".format(directory)
		isExists = os.path.exists(create_path)

		if not isExists:
			# 创建目录
			os.makedirs(create_path)  
			# 切换文件夹
			os.chdir(create_path)  
			return create_path
		else:
			return create_path

	def get_photo_list(self, num_pages):
		response = requests.get(self.start_url.format(num_pages), headers=self.headers)
		html_str = response.content.decode()
		html = json.loads(html_str)

		total = html["total"]
		total_pages = html["total_pages"]
		div_list = html["results"]
		photo_list = []

		for div in div_list:
			item = {}
			item["photo_id"] = div["id"]
			item["photo_width"] = div["width"]
			item["photo_height"] = div["height"]
			
			# 小图链接，测试用
			# item["download_url"] = div["urls"]["small"]
			
			item["download_url"] = div["links"]["download"]
			item["user_name"] = div["user"]["name"]
			photo_list.append(item)

		return total, total_pages, photo_list

	def save_photo_information(self, create_path, photo_list):
		file_path = r"{}/photo_information_{}.txt".format(create_path, self.photo_name)
		with open(file_path, "a", encoding="utf-8") as f:
			for photo in photo_list:
				f.write(json.dumps(photo, ensure_ascii=False, indent=2))
				f.write("\n")

	def download_photo(self, create_path, photo_list, total):
		for photo in photo_list:
			photo_id = photo["photo_id"]
			user_name = photo["user_name"]

			# 替换极少部分用户名存在的特殊字符
			for ch in (r'\/:*?"<>|'):
				user_name = user_name.replace(ch, "")

			download_url = photo["download_url"]
			print("Request: [{}] ".format(download_url), end=" >>> ")
			resp_photo = requests.get(download_url, headers=self.headers)
			print("Status code: [{}]".format(resp_photo.status_code))

			save_path = r"{}/{} Photo by {} on Unsplash.jpg".format(create_path, photo_id, user_name)
			with open(save_path, "wb") as f:
				f.write(resp_photo.content)
				print("Download [{}/{}] is complete!\n".format(self.num_photo, total))
				self.num_photo += 1

	def run(self):
		num_pages = 1
		total_pages = 2
		create_path = self.create_dir(self.photo_name)

		while num_pages <= total_pages:
			total, total_pages, photo_list = self.get_photo_list(num_pages)

			if len(photo_list) < 0:
				print("The keyword [{}] has no photos!".format(self.photo_name))
				break

			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), end=" >>> ")
			print("Crawling page [{}/{}].".format(num_pages, total_pages))

			self.save_photo_information(create_path, photo_list)
			self.download_photo(create_path, photo_list, total)
			num_pages += 1


if __name__ == '__main__':
	ekw = input("Please enter English keywords: ")
	print("Start download.")
	download_unsplash = DownloadUnsplash(ekw)
	download_unsplash.run()
	print("End of download.")

