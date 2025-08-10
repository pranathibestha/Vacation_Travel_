from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from email_utils import send_confirmation_email

app = Flask(__name__)
app.secret_key = 'travel_secret_key'

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///planner.db"
db = SQLAlchemy(app)

# ------------------- USER MODEL -------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# ------------------- DESTINATIONS -------------------
destinations = {
    'North India': {
        'Budget': [
            {'place':'Manali','food':500,'travel':3000,'stay':1000,
             'image':'https://i.ytimg.com/vi/7NKk41YVWyA/maxresdefault.jpg'},
            {'place':'Shimla','food':600,'travel':2500,'stay':1200,
             'image':'https://timesofindia.indiatimes.com/photo/52005539.cms'},
            {'place':'Dharamshala','food':550,'travel':2700,'stay':900,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRIqAZ3_xajTP6z_1DkkqjJT8QrHZL5vbKRP2xlNpn88QIE04lpPDTRcfqOGOHVFo7IWro&usqp=CAU'},
            {'place':'Kasol','food':500,'travel':2800,'stay':1100,
             'image':'https://media.istockphoto.com/id/908008144/photo/beautiful-view-of-himalayan-mountains-kasol-parvati-valley-himachal-pradesh-northern-india.jpg?s=612x612&w=0&k=20&c=1if08MeG1y2n73ha9VWqdnS_evyOl9Dgz-rNASvLxvM='},
            {'place':'Rishikesh','food':450,'travel':2200,'stay':950,
             'image':'https://s7ap1.scene7.com/is/image/incredibleindia/laxman%20jhula-rishikesh-uttrakhand-hero?qlt=82&ts=1726646312953'},
            {'place':'Haridwar','food':480,'travel':2100,'stay':900,
             'image':'https://media.istockphoto.com/id/825268350/photo/hardiwar.jpg?s=612x612&w=0&k=20&c=eCQt-N-2-wVm_imfNFtRyOPds8-NVLuoxTkHQ8N0ESg='}
        ],
        'Luxury': [
            {'place':'Manali','food':1000,'travel':6000,'stay':3000,
             'image':'https://i.ytimg.com/vi/7NKk41YVWyA/maxresdefault.jpg'},
            {'place':'Shimla','food':1200,'travel':5500,'stay':3200,
             'image':'https://timesofindia.indiatimes.com/photo/52005539.cms'},
            {'place':'Dharamshala','food':1050,'travel':5700,'stay':2900,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRIqAZ3_xajTP6z_1DkkqjJT8QrHZL5vbKRP2xlNpn88QIE04lpPDTRcfqOGOHVFo7IWro&usqp=CAU'},
            {'place':'Kasol','food':980,'travel':5800,'stay':3100,
             'image':'https://media.istockphoto.com/id/908008144/photo/beautiful-view-of-himalayan-mountains-kasol-parvati-valley-himachal-pradesh-northern-india.jpg?s=612x612&w=0&k=20&c=1if08MeG1y2n73ha9VWqdnS_evyOl9Dgz-rNASvLxvM='},
            {'place':'Rishikesh','food':900,'travel':5200,'stay':2800,
             'image':'https://s7ap1.scene7.com/is/image/incredibleindia/laxman%20jhula-rishikesh-uttrakhand-hero?qlt=82&ts=1726646312953'},
            {'place':'Haridwar','food':920,'travel':5100,'stay':2750,
             'image':'https://media.istockphoto.com/id/825268350/photo/hardiwar.jpg?s=612x612&w=0&k=20&c=eCQt-N-2-wVm_imfNFtRyOPds8-NVLuoxTkHQ8N0ESg='}
        ]
    },
    'South India': {
        'Budget': [
            {'place':'Munnar','food':400,'travel':2500,'stay':800,
             'image':'https://www.keralatourism.org/_next/image/?url=http%3A%2F%2F127.0.0.1%2Fktadmin%2Fimg%2Fpages%2Ftablet%2Fmunnar-blooms-blue-1743492906_7c09c3cad2add1e5fa89.webp&w=1920&q=75'},
            {'place':'Alleppey','food':450,'travel':2300,'stay':850,
             'image':'https://blog.untravel.com/wp-content/uploads/2017/04/Main-40.jpg'},
            {'place':'Ooty','food':420,'travel':2400,'stay':750,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRh3YgxmhDQZfvu9Ep_gUtgdqwnmRnpXo9VSA&s'},
            {'place':'Coorg','food':430,'travel':2600,'stay':800,
             'image':'https://c.ndtvimg.com/2025-05/hrgf60uo_coorg_625x300_17_May_25.jpg?im=FaceCrop,algorithm=dnn,width=1200,height=738'},
            {'place':'Hampi','food':390,'travel':2000,'stay':700,
             'image':'https://t4.ftcdn.net/jpg/03/75/40/73/360_F_375407347_spt4AF5sxsIt9gBIKVzJl95tiQhEGNXy.jpg'},
            {'place':'Mysore','food':410,'travel':2100,'stay':750,
             'image':'https://media.istockphoto.com/id/1281931838/photo/the-mysore-palace-at-night-in-mysore-in-southern-india.jpg?s=612x612&w=0&k=20&c=ylyE9VYrc008JnHKdXKDxbJx-_I2U8-oQFJDzwJk9Pw='}
        ],
        'Luxury': [
            {'place':'Munnar','food':950,'travel':5200,'stay':2400,
             'image':'https://www.keralatourism.org/_next/image/?url=http%3A%2F%2F127.0.0.1%2Fktadmin%2Fimg%2Fpages%2Ftablet%2Fmunnar-blooms-blue-1743492906_7c09c3cad2add1e5fa89.webp&w=1920&q=75'},
            {'place':'Alleppey','food':980,'travel':5000,'stay':2200,
             'image':'https://blog.untravel.com/wp-content/uploads/2017/04/Main-40.jpg'},
            {'place':'Ooty','food':920,'travel':5100,'stay':2300,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRh3YgxmhDQZfvu9Ep_gUtgdqwnmRnpXo9VSA&s'},
            {'place':'Coorg','food':940,'travel':5300,'stay':2500,
             'image':'https://c.ndtvimg.com/2025-05/hrgf60uo_coorg_625x300_17_May_25.jpg?im=FaceCrop,algorithm=dnn,width=1200,height=738'},
            {'place':'Hampi','food':880,'travel':4700,'stay':2100,
             'image':'https://t4.ftcdn.net/jpg/03/75/40/73/360_F_375407347_spt4AF5sxsIt9gBIKVzJl95tiQhEGNXy.jpg'},
            {'place':'Mysore','food':910,'travel':5400,'stay':2450,
             'image':'https://media.istockphoto.com/id/1281931838/photo/the-mysore-palace-at-night-in-mysore-in-southern-india.jpg?s=612x612&w=0&k=20&c=ylyE9VYrc008JnHKdXKDxbJx-_I2U8-oQFJDzwJk9Pw='}
        ]
    },
    'East India': {
        'Budget': [
            {'place':'Puri','food':420,'travel':2400,'stay':800,
             'image':'https://www.chanakyabnrpuri.com/wp-content/uploads/2024/12/Famous-Ancient-Temples-in-Puri.jpg'},
            {'place':'Konark','food':430,'travel':2200,'stay':850,
             'image':'https://www.savaari.com/blog/wp-content/uploads/2022/11/Konark-Sun-Temple-Ancient.webp'},
            {'place':'Bhubaneswar','food':400,'travel':2500,'stay':750,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwSCw8t2fbs3snbjjfh1JCOzsbW0D-a7qCWg&s'},
            {'place':'Darjeeling','food':440,'travel':2600,'stay':900,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJwY6TOS7xmRqJlkjeSDSWMgSyvgivri9HeA&s'},
            {'place':'Gangtok','food':450,'travel':2700,'stay':950,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRv1h2CW3z4jyZ5nOq9weM3H1nJ0rvYo8NPYA&s'},
            {'place':'Sundarbans','food':410,'travel':2300,'stay':700,
             'image':'https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Sundarban_Tiger.jpg/1200px-Sundarban_Tiger.jpg'}
        ],
        'Luxury': [
            {'place':'Puri','food':980,'travel':5100,'stay':2300,
             'image':'https://www.chanakyabnrpuri.com/wp-content/uploads/2024/12/Famous-Ancient-Temples-in-Puri.jpg'},
            {'place':'Konark','food':940,'travel':5000,'stay':2100,
             'image':'https://www.savaari.com/blog/wp-content/uploads/2022/11/Konark-Sun-Temple-Ancient.webp'},
            {'place':'Bhubaneswar','food':900,'travel':5200,'stay':2400,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwSCw8t2fbs3snbjjfh1JCOzsbW0D-a7qCWg&s'},
            {'place':'Darjeeling','food':1000,'travel':5500,'stay':2600,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJwY6TOS7xmRqJlkjeSDSWMgSyvgivri9HeA&s'},
            {'place':'Gangtok','food':1050,'travel':5700,'stay':2700,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRv1h2CW3z4jyZ5nOq9weM3H1nJ0rvYo8NPYA&s'},
            {'place':'Sundarbans','food':880,'travel':4800,'stay':2000,
             'image':'https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Sundarban_Tiger.jpg/1200px-Sundarban_Tiger.jpg'}
        ]
    },
    'West India': {
        'Budget': [
            {'place':'Udaipur','food':420,'travel':2500,'stay':850,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQifzOqlQY9jdFMZhyLe6Cq2mu6HtCH4VP89w&s'},
            {'place':'Jodhpur','food':430,'travel':2400,'stay':800,
             'image':'https://s7ap1.scene7.com/is/image/incredibleindia/2-mehrangarh-fort-jodhpur-rajasthan-city-hero?qlt=82&ts=1726660925514'},
            {'place':'Jaisalmer','food':440,'travel':2600,'stay':900,
             'image':'https://s7ap1.scene7.com/is/image/incredibleindia/1-bada-bagh-jaisalmer-rajasthan-attr-hero?qlt=82&ts=1727352831713'},
            {'place':'Mount Abu','food':450,'travel':2800,'stay':950,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxt6dlgtt7nPbBWnLzAnmNF7_YkJCbLtKd_Q&s'},
            {'place':'Kutch','food':470,'travel':2900,'stay':970,
             'image':'https://s7ap1.scene7.com/is/image/incredibleindia/rann-of-kutch-kutch-gujarat-1-attr-hero?qlt=82&ts=1726734017779'},
            {'place':'Goa','food':480,'travel':3000,'stay':1000,
             'image':'https://www.onthegotours.com/repository/beach-669.jpg'}
        ],
        'Luxury': [
            {'place':'Udaipur','food':900,'travel':5200,'stay':2400,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQifzOqlQY9jdFMZhyLe6Cq2mu6HtCH4VP89w&s'},
            {'place':'Jodhpur','food':920,'travel':5100,'stay':2300,
             'image':'https://s7ap1.scene7.com/is/image/incredibleindia/2-mehrangarh-fort-jodhpur-rajasthan-city-hero?qlt=82&ts=1726660925514'},
            {'place':'Jaisalmer','food':940,'travel':5300,'stay':2500,
             'image':'https://s7ap1.scene7.com/is/image/incredibleindia/1-bada-bagh-jaisalmer-rajasthan-attr-hero?qlt=82&ts=1727352831713'},
            {'place':'Mount Abu','food':1140,'travel':6400,'stay':3400,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxt6dlgtt7nPbBWnLzAnmNF7_YkJCbLtKd_Q&s'},
            {'place':'Kutch','food':980,'travel':6000,'stay':3000,
             'image':'https://s7ap1.scene7.com/is/image/incredibleindia/rann-of-kutch-kutch-gujarat-1-attr-hero?qlt=82&ts=1726734017779'},
            {'place':'Goa','food':1000,'travel':6200,'stay':3200,
             'image':'https://www.onthegotours.com/repository/beach-669.jpg'}
        ]
    },
    'Central India': {
        'Budget': [
            {'place':'Khajuraho','food':450,'travel':2800,'stay':900,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNemzzVQ4UCMR-JvvNhQcDqnq2FYJ2oi2weA&s'},
            {'place':'Bhopal','food':400,'travel':2500,'stay':850,
             'image':'https://t3.ftcdn.net/jpg/04/73/45/68/360_F_473456829_OtAjHyQQs8eXxagx8SCIo9m0rBqIbIoz.jpg'},
            {'place':'Indore','food':420,'travel':2400,'stay':800,
             'image':'https://content.r9cdn.net/rimg/dimg/81/27/f9da72b6-city-18952-169edddbd24.jpg?width=1200&height=630&xhint=2118&yhint=1521&crop=true'},
            {'place':'Pachmarhi','food':430,'travel':2600,'stay':900,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcCek4FUOujSQOtodEMtliDjQaTUoaGdrNZQ&s'},
            {'place':'Jabalpur','food':410,'travel':2700,'stay':880,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqaqqzNa5WvNkEP77MNlkog1kL9HvCKKKICA&s'},
            {'place':'Sanchi','food':390,'travel':2200,'stay':800,
             'image':'https://media.istockphoto.com/id/2149703338/photo/the-great-stupa-at-sanchi-india.jpg?s=612x612&w=0&k=20&c=jTq6BPsdEBCRDBD9f8vZuR5Alzt1lxUwamGksgvwON4='}
        ],
        'Luxury': [
            {'place':'Khajuraho','food':950,'travel':5700,'stay':2600,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNemzzVQ4UCMR-JvvNhQcDqnq2FYJ2oi2weA&s'},
            {'place':'Bhopal','food':900,'travel':5200,'stay':2400,
             'image':'https://t3.ftcdn.net/jpg/04/73/45/68/360_F_473456829_OtAjHyQQs8eXxagx8SCIo9m0rBqIbIoz.jpg'},
            {'place':'Indore','food':920,'travel':5100,'stay':2300,
             'image':'https://content.r9cdn.net/rimg/dimg/81/27/f9da72b6-city-18952-169edddbd24.jpg?width=1200&height=630&xhint=2118&yhint=1521&crop=true'},
            {'place':'Pachmarhi','food':940,'travel':5300,'stay':2500,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcCek4FUOujSQOtodEMtliDjQaTUoaGdrNZQ&s'},
            {'place':'Jabalpur','food':910,'travel':5400,'stay':2450,
             'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqaqqzNa5WvNkEP77MNlkog1kL9HvCKKKICA&s'},
            {'place':'Sanchi','food':880,'travel':5000,'stay':2200,
             'image':'https://media.istockphoto.com/id/2149703338/photo/the-great-stupa-at-sanchi-india.jpg?s=612x612&w=0&k=20&c=jTq6BPsdEBCRDBD9f8vZuR5Alzt1lxUwamGksgvwON4='}
        ]
    },
    'Northeast India': {
    'Budget': [
        {'place':'Shillong','food':450,'travel':2800,'stay':900,
         'image':'https://s3.india.com/wp-content/uploads/2024/03/Feature-Image_-Hidden-Charms-of-Shillong.jpg?impolicy=Medium_Widthonly&w=330'},
        {'place':'Cherrapunji','food':460,'travel':2900,'stay':950,
         'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgmU6R2hFVVtBWyC2FfozMCvPkZzhDY1ZmwA&s'},
        {'place':'Tawang','food':470,'travel':3100,'stay':1000,
         'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRf2hXokrwWZNlNNgSChkFMLWJkCTFpKQBlkw&s'},
        {'place':'Imphal','food':440,'travel':2700,'stay':850,
         'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTabCkpPx02q3woL4RrpMaRNYbq6YPhHQt0g&s'},
        {'place':'Aizawl','food':430,'travel':2600,'stay':800,
         'image':'https://xplro.com/wp-content/uploads/2024/07/Xplro-2024-07-26T002602.142.jpg'},
        {'place':'Agartala','food':420,'travel':2500,'stay':780,
         'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhkBHG7aJEmbUul0EeCwiGXfqjxz9S1PBLOGSJTPqXH9LV0JY7v8mGyXwA7mrDrmTCKtA&usqp=CAU'}
    ],
    'Luxury': [
        {'place':'Shillong','food':980,'travel':5800,'stay':2500,
         'image':'https://s3.india.com/wp-content/uploads/2024/03/Feature-Image_-Hidden-Charms-of-Shillong.jpg?impolicy=Medium_Widthonly&w=330'},
        {'place':'Cherrapunji','food':1000,'travel':6000,'stay':2700,
         'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgmU6R2hFVVtBWyC2FfozMCvPkZzhDY1ZmwA&s'},
        {'place':'Tawang','food':1050,'travel':6200,'stay':2900,
         'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRf2hXokrwWZNlNNgSChkFMLWJkCTFpKQBlkw&s'},
        {'place':'Imphal','food':950,'travel':5600,'stay':2300,
         'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTabCkpPx02q3woL4RrpMaRNYbq6YPhHQt0g&s'},
        {'place':'Aizawl','food':940,'travel':5500,'stay':2200,
         'image':'https://xplro.com/wp-content/uploads/2024/07/Xplro-2024-07-26T002602.142.jpg'},
        {'place':'Agartala','food':930,'travel':5400,'stay':2100,
         'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhkBHG7aJEmbUul0EeCwiGXfqjxz9S1PBLOGSJTPqXH9LV0JY7v8mGyXwA7mrDrmTCKtA&usqp=CAU'}
    ]
}

}


# ------------------- ROUTES -------------------
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["name"] = user.name
            session["email"] = user.email
            flash("Login successful!", "success")
            return redirect(url_for("regions"))
        else:
            flash("Invalid email or password!", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for("register"))
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route('/regions')
def regions():
    if "user_id" not in session:
        return redirect(url_for('login'))
    return render_template('regions.html', destinations=destinations)

@app.route('/packages/<region>')
def packages(region):
    if "user_id" not in session:
        return redirect(url_for('login'))
    if region in destinations:
        return render_template('packages.html', region=region, data=destinations[region])
    return "Region not found"

@app.route('/details/<region>/<package>/<place>')
def details(region, package, place):
    if "user_id" not in session:
        return redirect(url_for('login'))
    for dest in destinations[region][package]:
        if dest['place'] == place:
            return render_template('details.html', dest=dest, package=package, region=region)
    return "Destination not found"

@app.route('/payment', methods=['POST'])
def payment():
    if "user_id" not in session:
        return redirect(url_for('login'))
    session['selected'] = {
        'region': request.form['region'],
        'package': request.form['package'],
        'place': request.form['place'],
        'food': int(request.form['food']),
        'travel': int(request.form['travel']),
        'stay': int(request.form['stay']),
        'persons': int(request.form['persons']),
    }
    total = (session['selected']['food'] +
             session['selected']['travel'] +
             session['selected']['stay']) * session['selected']['persons']
    session['selected']['total'] = total
    return render_template('payment.html', total=total)

@app.route('/confirm', methods=['POST'])
def confirm():
    if "user_id" not in session:
        return redirect(url_for('login'))
    send_confirmation_email(
        to=session['email'],
        name=session['name'],
        place=session['selected']['place'],
        total=session['selected']['total']
    )
    return render_template('success.html',
                           name=session['name'],
                           email=session['email'],
                           booking=session['selected'])
@app.route('/get', methods=['POST'])
def chatbot_reply():
    user_message = request.json.get("message")
    # Simple rule-based logic (can be extended)
    if "hello" in user_message.lower():
        reply = "Hello! How can I assist you with your travel plans today?"
    elif "package" in user_message.lower():
        reply = "We offer both Budget and Luxury packages across India. Visit the regions page after login to explore."
    elif "price" in user_message.lower() or "cost" in user_message.lower():
        reply = "Each package cost includes travel, food, and stay, and is shown per person. You can check the breakdown on the package detail page."
    elif "email" in user_message.lower():
        reply = "After payment, you'll get a confirmation email with all booking details."
    else:
        reply = "I'm here to help! Please ask about destinations, packages, or booking steps."
    return jsonify({"response": reply})


if __name__ == '__main__':
    app.run(debug=True)

