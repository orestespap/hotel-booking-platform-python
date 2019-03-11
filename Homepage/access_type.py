import Homepage.user
import Homepage.hotel
import Homepage.admin

def select_account_type():
    func_dict={'u':Homepage.user.log_in, 'a':Homepage.admin.log_in, 'h':Homepage.hotel.log_in, 'e':exit}
    maintext='Select one of the following:\nUSER [U]\nHOTEL [H]\nADMIN [A]\nEXIT [E]\nChoice: '
    ans=input(maintext)
    while ans.lower() not in 'uhae':
        ans=input(maintext)

    func_dict[ans]()