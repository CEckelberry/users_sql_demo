"""Seed file to make sample data for pets db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add Users
john = User(
    first_name="John",
    last_name="Smith",
    image_url="https://vignette.wikia.nocookie.net/disney/images/5/5e/Profile_-_John_Smith.png/revision/latest?cb=20190312150145",
)
carol = User(
    first_name="Carol",
    last_name="Pain",
    image_url="https://www.abc.net.au/cm/rimage/11806990-3x2-xlarge.jpg?v=3",
)
captain = User(
    first_name="Captain",
    last_name="America",
    image_url="https://cdn.shopify.com/s/files/1/1343/0857/products/POP0054AB1_604d0ca3-5346-4720-89d1-859d2d1bfd79.jpg?v=1571610468",
)


political = Post(
    title="Yay Biden Harris!",
    content="I can't believe we are going to have the first female VP this year! What a historic event to be apart of in shit 2020",
    user_id=1,
)
political2 = Post(
    title="2020 Election", content="This is getting really close", user_id=1
)

funny = Post(
    title="Hilarious Dog Story",
    content="My dog is such a goober that he likes to stretch out and rub his belly on the carpet.",
    user_id=3,
)

funny2 = Post(
    title="Silly Cat Story",
    content="My cat likes to show everyone his butthole!",
    user_id=2,
)

sad = Post(
    title="Mother passed",
    content="My mom passed away, and I don't know how I should feel?",
    user_id=2,
)

angry = Post(
    title="Why do Spiders Exist?",
    content="Don't you guys just want to stomp all of them to death?",
    user_id=3,
)


# Add new objects to session, so they'll persist
db.session.add(john)
db.session.add(carol)
db.session.add(captain)

# Commit--otherwise, this never gets saved!
db.session.commit()
# Add new Posts after users
db.session.add(political)
db.session.add(political2)
db.session.add(funny)
db.session.add(funny2)
db.session.add(sad)
db.session.add(angry)
# Commit--otherwise, posts never gets saved!
db.session.commit()
