class Blog:
    def __init__(self):
        self.users = set()
        self.posts = []
        self.current_user = None

    def __get_post_from_id(self, post_id):

        for post in self.posts:
            print(post.id)
            if post.id == post_id:
                return post
        
    

    def create_new_user(self):
        username = input("Please enter a username: ")

        if username in {u.username for u in self.users}:
            print(f"User with username {username} already exists")
        else:
            password = input("Please enter your password. ")
            user = User(username, password)
            self.users.add(user)
            print(f"{user} has been created!!!")

    def log_user_in(self):
        username = input("What is your username? ")
        password = input("What is your password? ")

        for user in self.users:
            if user.username == username and user.check_password(password):
                self.current_user = user
                print(f"{user} has logged in")
                break
        else:
            print("Username and/or password is incorrect")

    def log_user_out(self):
        self.current_user = None
        print("You have successfully logged out!")

    def create_new_post(self):
        if self.current_user:
            title = input("Enter the title of your post: ")
            body = input("Enter thebody of your post:")

            new_post = Post(title, body, self.current_user)
            for user in self.users:
                if user.username == self.current_user.username:
                    user.posts.append(new_post)

            self.posts.append(new_post)
            print(f"{new_post.title} has been created!")
        else:
            print("No user logged in. Please log in before making a post.")
            return

    def view_current_user_posts(self):
        if self.current_user:
            for user in self.users:
                if user.username == self.current_user.username:
                    if user.posts:
                        print(f"{self.current_user} posts:")
                        for post in user.posts:
                            print(post)
                    else:
                        print("There are currently no posts for this user :(")
        else:
            print("No users currently signed in. Sign in to view posts")

    def view_all_posts(self):
        if self.posts:
            for post in self.posts:
                print(post)
        else:
            print("There are currently no posts for this blog")


    def view_post(self, post_id):
        post = self.__get_post_from_id(post_id)
        if post:
            print(post)
        else:
            print(f"Post with id {post_id} does not exist")

    def edit_post(self, post_id):
        post = self.__get_post_from_id(post_id)
        if post:
            if self.current_user and self.current_user == post.author:
                print(post)

                new_title = input("Please enter the new title or enter skip to keep the current title")
                if new_title.lower() != 'skip':
                    post.title = new_title
                new_body = input("Please enter the new body of the post of enter skip to keep current body")
                if new_body.lower() != 'skip':
                    post.body = new_body
                print(f"{post.title} has been updated")

            elif self.current_user and self.current_user != post.author:
                print("You do not have permission to edit this post.") # 403 Forbidden
            else:
                print("You must be logged in to perform this action") #401 Unauthorized
        else:
            print(f"Post with an ID of {post_id} does not exist") # 404 Not Found

    def delete_post(self, post_id):
        post = self.__get_post_from_id(post_id)
        if post:
            if self.current_user and self.current_user == post.author:
                print(post)
                you_sure = input("Are you sure you wnat to delete this post? Enter 'yes' to delete")
                if you_sure.lower() == 'yes':
                    self.posts.remove(post)
                    print(f"{post.title} has been removed from the blog")
                else:
                    print("Okay we won't delete this post")
            elif self.current_user and self.current_user != post.author:
                print("You do not have permission to delete this post.") # 403 Forbidden
            else:
                print("You must be logged in to perform this action") #401 Unauthorized



class User:
    id_counter = 1
    def __init__(self, username, password):
        self.username = username
        self.password = password[::-2]
        self.id = User.id_counter
        User.id_counter += 1
        self.posts = []
    def __str__(self):
        return self.username
    
    def __repr__(self):
        return f"<User {self.id} | {self.username}>"
    
    def check_password(self, password_guess):
        return self.password == password_guess[::-2]

class Post:
    id_counter = 1
    
    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author
        self.id = Post.id_counter
        Post.id_counter += 1

    def __repr__(self):
        return f"<Post {self.id} | {self.title}>"
    
    def __str__(self):
        formatted_post = f"""
        {self.id} - {self.title.title()}
        By: {self.author}
        {self.body}
        """
        return formatted_post


def run_blog():
    my_blog = Blog()

    while True:
        # menu options for not logged in users
        if not my_blog.current_user: 
            print("Welcome to my blog!")
            print("1. Sign UP\n2. Log In3. View All Post\n4. View Single Post\n5. Quit")
            to_do = input("Which option would you like to do? ")

            while to_do not in {'1','2','3','4','5'}:
                to_do = input("Invalid OPtion. Please choose 1,2,3,4,5")

            if to_do == '5':
                print("Thanks for checking out the blog")
                break
            elif to_do == '1':
                my_blog.create_new_user()

            elif to_do == '2':
                my_blog.log_user_in()
            
            elif to_do == '3':
                my_blog.view_all_posts()

            elif to_do == '4':
                post_id = input("What is the id of your post? ")
                my_blog.view_post(post_id)

            elif to_do == '5':
                break

        # menu options for logged in user
        else:
            print("1.Log Out\n2. Create New Post\n3. View Your Posts\n4. View All Posts\n5. View Single Post\n6. Edit a Post\n7. Delete a Post")
            to_do = input("Which option would you like to do? ")
            while to_do not in {'1','2','3','4','5','6','7'}:
                to_do = input("Invalid Option. Please choose 1,2,3,4,5,6,7:")
            if to_do == '1':
                my_blog.log_user_out()
            elif to_do == '2':
                my_blog.create_new_post()
            elif to_do == '3':
                my_blog.view_current_user_posts()
            elif to_do == '4':
                my_blog.view_all_posts()
            elif to_do == '5':
                post_id = input("What is the id of your post? ")
                while not post_id.isdigit():
                    post_id = input('Invalid ID. Please enter a number')
                my_blog.view_post(post_id)
            elif to_do == '6':
                post_id = input("What is the Id of your post?")
                while not post_id.isdigit():
                    post_id = input('Invalid ID. Please enter a number')
                my_blog.edit_post(post_id)
            elif to_do == '7':
                post_id = input("What is the Id of your post?")
                while not post_id.isdigit():
                    post_id = input('Invalid ID. Please enter a number')
                my_blog.delete_post(post_id)



run_blog()