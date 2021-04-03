import pandas as pd

df = pd.read_json('contacts.json')

#printing connected tickets to check on RCR (Repeat Contact Rate)
print(df.iloc[1])
print(df.iloc[2458])
print(df.iloc[98519])
print(df.iloc[115061])
print(df.iloc[476346])


# print(df.head())
# exit()

users = {}
emails = {}
phones = {}
orderids={}

class User:
    def __init__(self, userid):
        self.emails = []
        self.phones = []
        self.orderids = []
        self.userid = userid
        self.ticketids =[]
        self.contacts = []

    def prnt(self):
        print("The user id is ", self.userid)
        print("The emails are ", self.emails)
        print("The phones are ", self.phones)
        print("The orderids are ", self.orderids)
        print("The contacts are ", self.contacts)
        print("The ticketids are ", self.ticketids)

print("Made")
myuserid= 0
for ind in df.index:
    #get details
    ticket = df.loc[ind]
    email = ticket['Email']
    phone = ticket['Phone']
    orderid = ticket['OrderId']
    ticketid = ticket['Id']
    contacts = ticket['Contacts']

    print(ind)

    userExists = False
    orderExists = False
    emailExists = False
    phoneExists = False

    #check if any detail exists, thus implying user was found previously

    userObj = ""
    if orderid in orderids:
        userObj = users[orderids[orderid]]
        userExists = True
        orderExists = True

    if email in emails:
        userObj = users[emails[email]]
        userExists = True
        emailExists = True

    if phone in phones:
        userObj = users[phones[phone]]
        userExists = True
        phoneExists = True
    
    if not userExists:
        print("New User")
        user = User(myuserid) #create new user
        if orderid != "":
            user.orderids.append(orderid)
            orderids[orderid] = myuserid

        if email != "":
            user.emails.append(email)
            emails[email] = myuserid

        if phone != "":
            user.phones.append(phone)
            phones[phone] = myuserid

        user.ticketids.append(ticketid)
        user.contacts.append(contacts)
        users[myuserid] = user

        myuserid = myuserid + 1

        # user.prnt()

    else:
        print("Existing User")

        if email != "" and not emailExists:
            emails[email] = userObj.userid
            userObj.emails.append(email)

        if orderid != "" and not orderExists:
            orderids[orderid] = userObj.userid
            userObj.orderids.append(orderid)

        if phone != "" and not phoneExists:
            phones[phone] = userObj.userid
            userObj.phones.append(phone)


        userObj.contacts.append(contacts)
        userObj.ticketids.append(ticketid)


manualid = 1
finalList = []
class Results:
    def __init__(self, id, res):
        self.id = id
        self.res = res

for i in range(len(df)):
    finalList.append(Results(i+1, ""))
    manualid = manualid + 1


for id,user in users.items():
    chain = ""
    for iid in user.ticketids:
        if user.ticketids[len(user.ticketids)-1] == iid: #last item
            chain = chain + str(iid)
        else:
            chain =  chain+ (str(iid)+"-")
    
    sumCon = 0
    for con in user.contacts:
        sumCon = sumCon + int(con)
    
    chain = chain+ "," + str(sumCon)

    for iid in user.ticketids:
        finalList[int(iid) - 1].res = chain

i=0
finalCSVList = []
for item in finalList:
    print("Creating List")
    finalCSVList.append([item.id, item.res])
    i = i + 1

print(finalCSVList[:20])
df = pd.DataFrame(finalCSVList, columns = ['ticket_id', 'ticket_trace/contact'])
print(df)
df.to_csv('/Users/prakash/Desktop/outputsssss.csv')
