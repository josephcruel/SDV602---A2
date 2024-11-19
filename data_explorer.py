import sys
from view import chat_view
sys.dont_write_bytecode = True
from view.login_user import LoginView
from view.chat_view import ChatView



if __name__ == "__main__" :
    """
    Code that runs when this is the main module.
    """
    #des_obj = DES_View()
    #des_obj.set_up_layout()
    #des_obj.render()
    
    #des_obj.accept_input()

    login_view = LoginView()
    login_view.set_up_layout()
    login_view.render()
    login_view.accept_input()

    pass