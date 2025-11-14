# Concurrency example using multiple implementations
# Example searches for a topic on wikipedia, gets related topics and 
#   saves the references from related topics in their own text file
# info on wikipedia library: https://thepythoncode.com/article/access-wikipedia-python
# info on concurrent.futures library: https://docs.python.org/3/library/concurrent.futures.html#

import time
import wikipedia
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os
import re

#convert objects produced by wikipedia package to a string var for saving to text file
def convert_to_str(obj):
	if isinstance(obj, list):
		mystr = "\n".join([str(item) for item in obj])
		return mystr
	elif isinstance(obj, (str, int, float)):
		return str(obj)


# IMPLEMENTATION 1: sequential example
def wiki_sequentially(search, dir_path):
	print("\nsequential function:")
	t_start = time.perf_counter()
	try:
		results = wikipedia.search(search)
	except Exception as e:
		print("Error Searching Wikipedia:", e)
	
	for item in results:
		try:
			page = wikipedia.page(item, auto_suggest=False)
		except wikipedia.exeption.DisambiguationError as e:
			print(f"Error Skipping '{item}': {e}")
			continue
		except wikipedia.exceptions.PageError:
			print(f"Page '{item}' Not Found: {e}")
			continue
		except Exception as e:
			print(f"Error '{item}': {e}")
			continue
		
		title = page.title
		title = re.sub(r"[\\/*?:\"'<>|\s\x00-\x1F\x7F]", "_", title) # Ensures safe filename
		references = convert_to_str(page.references)

		out_filename = title + ".txt"
		out_filename = os.path.join(dir_path, out_filename)
		print(f"writing to {out_filename}")
		try:
			with open(out_filename, "w", encoding="utf-8") as fileobj:
				fileobj.write(references)
		except Exception as e:
			print(f"Failed Writing To '{out_filename}': {e}")

	t_end = time.perf_counter()
	t_lapse = t_end - t_start
	print(f"code executed in {t_lapse} seconds")

# IMPLEMENTATION 2: concurrent example w/ threads
def concurrent_threads():
	print("\nthread pool function:")
	t_start = time.perf_counter()
	results = wikipedia.search("general artificial intelligence")

	def dl_and_save_thread(item):
		page = wikipedia.page(item, auto_suggest=False)
		title = page.title
		references = convert_to_str(page.references)
		out_filename = title + ".txt"
		print(f"writing to {out_filename}")
		with open(out_filename, "w") as fileobj:
			fileobj.write(references)

	with ThreadPoolExecutor() as executor:
		executor.map(dl_and_save_thread, results)

	t_end = time.perf_counter()
	t_lapse = t_end - t_start
	print(f"code executed in {t_lapse} seconds")

# IMPLEMENTATION 3: concurrent example w/ processes
#  processes do not share memory; multiprocessing and concurrent.futures.ProcessPoolExecutor pickle
#  objects in order to communicate - can"t pickle nested functions so must structure accordingly
def dl_and_save_process(item): # moved to module level in this example due to processes not sharing memory
	page = wikipedia.page(item, auto_suggest=False)
	title = page.title
	references = convert_to_str(page.references)
	out_filename = title + ".txt"
	print(f"writing to {out_filename}")
	with open(out_filename, "w") as fileobj:
		fileobj.write(references)

def concurrent_process():
	print("\nprocess pool function:")
	t_start = time.perf_counter()
	results = wikipedia.search("general artificial intelligence")

	with ProcessPoolExecutor() as executor:
		executor.map(dl_and_save_process, results)

	t_end = time.perf_counter()
	t_lapse = t_end - t_start
	print(f"code executed in {t_lapse} seconds")


def main():
	# Create Directory
	dir_path = os.path.join(os.path.dirname(__file__), "wiki_dl")
	os.makedirs(dir_path, exist_ok=True)
	
	# Get Input
	print("Search for References from Wikipedia Pages")
	search = input("Enter: ")

	if len(search) < 4: tisearchtle = "generative artificial intelligence"
	



	wiki_sequentially(search, dir_path)
	#concurrent_threads()
	#concurrent_process()
	return

if __name__ == "__main__":
	main()