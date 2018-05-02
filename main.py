from response_modules import response_module

if __name__ == '__main__':

    current_question = "BEGIN"

    while current_question != "END":

        if current_question == "BEGIN":
            current_question = input("Hi I'm Milo, What I can do for you? \n")
        else:
            if current_question != "END":
                response = response_module.process_message(current_question)
                current_question = input(response + "\n")

