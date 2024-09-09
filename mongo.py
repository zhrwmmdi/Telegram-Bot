# from pymongo import MongoClient
#
# client = MongoClient('mongodb://localhost:27017/')
#
# db = client['QueraDatabase']
#
#
# collection = db['users']
#
# user1 = {'name': 'SAliB', 'age': 30, 'email': 'salib@example.com'}
# user2 = {'name': 'Bagher', 'age': 25, 'email': 'bagher@example.com'}
#
# result = collection.insert_one(user1)
# print('Inserted id:', result.inserted_id)
#
# result = collection.insert_many([user2])
# print('Inserted ids:', result.inserted_ids)
#
#
# result = collection.find_one({'name': 'SALiB'})
# print('Found document:', result)
#
# results = collection.find()
# print('All documents:')
# for document in results:
#     print(document)
#
# collection.update_one({'name': 'SALiB'}, {'$set': {'age': 35}})
#
# collection.update_many({"age": {"$lt": 18}}, {"$set": {"status": "Inactive"}})
#
# collection.delete_one({'name': 'Bagher'})
#
# collection.delete_many({"age": {"$gt": 30}})


if  __name__ == '__main__':
    list= [100, 'category', 'this', 'is',  'a',  'description']
    amount = list[0]
    category = list[1]
    description = ' '.join(list[2:])

    print(amount)
    print(category)
    print(description)

