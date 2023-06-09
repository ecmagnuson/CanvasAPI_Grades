![gif](./example.gif)

Initially I used a Canvas API Python repository that is on [github](https://github.com/ucfopen/canvasapi), but for this project I want to directly use the [requests](https://pypi.org/project/requests/) library. My original project that I wrote a while ago is in the `old` directory. This new one makes use of a custom object I made in canvas.py that uses a modified get request via the requests package. I spent a significant time going through the actual [Canvas LMS REST API](https://canvas.instructure.com/doc/api/) to figure out the URLs I would need to call to get the information I needed. 

I created this program to allow me to selectively download the assignments of students that are in the specific section of a class that I TA. It runs in the command prompt. The main file to rune to enter the program is `main.py`.  

This program is procedural. After running it, it does the following:
1. Prompt get a course (required)
2. Prompt get a section (this is not required)
3. Prompt get groups in course or section (this is not required)
4. Get a specific assignment (required)
5. Prompt a specific name to be added to every assignment as it is renamed
6. Download that assignment to each students prepared directory, and copy any files from the `resources` directory there as well

* It will only show you classes where you are a teacher or TA
* It is not required to get only students in one section, or their groups info, but I make use of this (as can be seen in the gif)
* It prompts you for only assignments that are visible to students and that have not been graded
* It allows you to rename the assignments to anything you want, but defaults to original student assignment names when there is more than 1 submission for an assignment
* Inside of the `resources` directory you can place any file you want, and it will be copied into each students directory. I place my grading sheets in there.
 

## How to use this program:

1. `pip install -r requirements.txt` to install the requests library
2. In auth.json set your API_URL accordingly:
	- API_URL is your url for Canvas plus "/api/v1"
	- i.e. "https://canvas.wisc.edu/api/v1"
	- If you are using UW Madison Canvas it is already set
	
3. In auth.json set your API_KEY accordingly:
	- On the left hand side of your Canvas home page:
		+ [Account > Settings](https://canvas.wisc.edu/profile/settings)
		
 	- Scroll down and click "New Access Token"
 	- Give it a name and expiration date 
 	- Generate token
	 	+ It will be a long string of characters
 	- Copy down the token and put it into auth.json API_KEY
	- i.e. : "8dj2j3j5k4k399dkdmkdmslsldfkjsdflsdfl"
	- Keep the quotes in auth.json
 	
4. Any file that you place into the `resources` directory will be copied into each students assignment, so if you have any sort of rubric or feedback sheet you can place it there.
5. Run the program and it will guide you through the process inside of a terminal. This can be seen in the example gif above.

