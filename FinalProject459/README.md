## How to use this program:

1. In Auth.txt set your API_URL accordingly:
	- API_URL is your url for Canvas
	- i.e. "https://canvas.wisc.edu/"
	
2. In Auth.txt set your API_KEY accordingly:
	- On the left hand side of your Canvas home page:
		+ Account > Settings
		
 	- Scroll down and click "New Access Token"
 	- Give it a name and expiration date 
 	- Generate token
	 	+ It will be a long string of characters
 	- Copy down the token and put it into Auth.txt API_KEY
	- i.e. : "8dj2j3j5k4k399dkdmkdmslsldfkjsdflsdfl"
	- Keep the quotes in Auth.txt
 	
3. Any file that you place into the `resources` directory will be copied into each students assignment, so if you have any sort of rubric or feedback sheet you can place it there.
4. Run the program and it will guide you through the process inside of a terminal.


--------------------

# TODO 

1. It's really messy so it needs to be refactored
2. I don't account for if a submission was late
3. I haven't checked for comments
4. I haven't checked for multiple submissions or newest submissions
5. I gave this program to my other TA's to use, but I didn't program it defensively enough, so that if for example they give it a value that is not accepted it will crash and throw an unintelligable error to them vs. saying something like "invalid response, enter the number corresponding to the class you want to pick", etc
6. I need to do the same for accepting the API key, and the error it throws if it is invalid
7. I want to figure out only showing assignments that require students to submit files. For example, I shouldn't see a prompt about downloading files from an in canvas quiz that doesn't require a submission and is graded automatically.

