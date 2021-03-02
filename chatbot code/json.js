import { MongoClient } from 'mongodb'

export async function connect () {
  // Connection URL
  const url = 'mongodb+srv://jaga:Chatbot@test.jzk8s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

  let db

  try {
    db = await MongoClient.connect(url)
    console.log('Connected successfully!')
  } catch (err) {
    // Handle error
  }

  return db
}