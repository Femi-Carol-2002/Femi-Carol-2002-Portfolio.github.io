from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# SECURITY: Validate secret key exists
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    raise ValueError("No SECRET_KEY set in .env file")
app.secret_key = secret_key

# Email configuration with validation
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'True').lower() == 'true',
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER') or os.getenv('MAIL_USERNAME')
)

# Corrected email credentials validation
if not all([app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']]):
    raise ValueError("Missing email credentials in .env")

mail = Mail(app)

# Project details data

projects = {
    'breast-cancer': {
        "title": "Breast Cancer Classification And Localization Of Tumour",
        "category": "AI/ML",
        "main_image": "images/breast-cancer-thumbnail.jpg",
        "date": "Nov 2024 - Apr 2025",
        "duration": "6 months",
        "team_size": "Solo",
        "description": "Developed a deep learning system combining EfficientNet and YOLO for accurate breast tumor classification and localization in mammograms.",
        "problem_statement": "Traditional diagnostic methods rely heavily on radiologists, leading to variability in interpretation. Existing AI solutions often lack both classification accuracy and precise tumor localization.",
        "metrics": [
            {"value": "93.6%", "label": "Classification Accuracy"},
            {"value": "89.4%", "label": "mAP@0.5"},
            {"value": "0.82", "label": "IoU Score"},
            {"value": "94.8%", "label": "Recall"}
        ],
        "technologies": ["Python", "TensorFlow", "EfficientNet", "YOLOv5", "Flask", "OpenCV", "Pandas"],
        "solution": "Integrated EfficientNet for tumor classification (benign/malignant) with YOLO for precise tumor localization, creating an end-to-end diagnostic pipeline.",
        "methodology": [
            "Collected and annotated 5GB mammogram dataset (CBIS-DDSM, INbreast)",
            "Preprocessed images with CLAHE and median filtering",
            "Implemented hybrid architecture with shared feature extraction",
            "Trained with balanced loss function (cross-entropy + MSE)",
            "Deployed as Flask web app with diagnostic report generation"
        ],
        "challenges": [
            {
                "challenge": "Small tumor detection in high-res images",
                "solution": "Optimized YOLO anchor boxes and trained on high-IoU annotations"
            },
            {
                "challenge": "Class imbalance in medical data",
                "solution": "Applied class weighting and strategic data augmentation"
            }
        ],
        "visuals": [
            {"image": "images/breast-cancer-1.png", "caption": "Web interface for diagnosis"},
            {"image": "images/breast-cancer-2.png", "caption": "Tumor detection with bounding boxes"},
            {"image": "images/breast-cancer-3.png", "caption": "Characteristics of the Tumor"},
            {"image": "images/breast-cancer-4.png", "caption": "Performance metrics dashboard"}  
        ],
        "outcomes": [
            "Achieved 93.6% classification accuracy (6.3% improvement over baseline)",
            "Reduced false negatives by 11.1% compared to radiologist benchmarks",
            "Developed real-time analysis system with 77ms average inference time",
            "Generated comprehensive diagnostic reports with tumor characteristics"
        ],
        "impact": "The system reduces radiologist workload by 40% for preliminary screenings while maintaining 98.2% agreement with expert diagnoses.",
        "lessons": [
            "Importance of domain-specific preprocessing in medical imaging",
            "Trade-offs between model complexity and deployment feasibility",
            "Value of explainable AI in healthcare applications"
        ],
        "future_improvements": [
            "Multi-class tumor classification (ductal/lobular carcinoma)",
            "Integration with hospital PACS systems",
            "Federated learning for privacy-preserving model improvements"
        ],
        "github_link": "#",
        "live_link": "#",
        "report_link": "#"
    },
    'expense-prediction': {
        "title": "Managing Monthly Expenses Prediction",
        "category": "Data Science",
        "main_image": "images/expense-thumbnail.jpg",
        "date": "June 2024 - Nov 2024",
        "duration": "5 months",
        "team_size": "Solo",
        "description": "Machine learning system to predict individuals' ability to manage monthly expenses based on income and spending patterns.",
        "problem_statement": "Many people struggle with financial planning due to unpredictable expenses and lack of personalized budgeting tools.",
        "metrics": [
            {"value": "93%", "label": "Best Model Accuracy"},
            {"value": "0.91", "label": "F1-Score"},
            {"value": "101", "label": "Survey Responses"},
            {"value": "8", "label": "ML Models Tested"}
        ],
        "technologies": ["Python", "Scikit-learn", "XGBoost", "Pandas", "Matplotlib", "Excel"],
        "solution": "Developed a comparative analysis of multiple ML algorithms to predict budget management success from survey data.",
        "methodology": [
            "Designed and distributed Google Forms survey (101 respondents)",
            "Preprocessed data with ordinal encoding and outlier removal",
            "Compared 8 algorithms (XGBoost, Random Forest, KNN, etc.)",
            "Optimized hyperparameters using grid search",
            "Analyzed feature importance for financial insights"
        ],
        "challenges": [
            {
                "challenge": "Small dataset with self-reported values",
                "solution": "Applied rigorous cross-validation and class balancing"
            },
            {
                "challenge": "Categorical feature interpretation",
                "solution": "Developed intuitive ordinal encoding system"
            }
        ],
        "visuals": [
            {"image": "images/expense-1.png", "caption": "Comparison of different models metrix"},
            {"image": "images/expense-2.png", "caption": "Confusion Matrix"},
            {"image": "images/expense-3.png", "caption": "Survey data distribution"},
            {"image": "images/expense-4.png", "caption": "Average Spending (Bar Chart)"}
        ],
        "outcomes": [
            "Identified XGBoost as top performer (93% accuracy)",
            "Discovered key predictors: savings rate > income > utilities",
            "40% of respondents struggled with budget management",
            "Created actionable financial planning insights"
        ],
        "impact": "The model helps financial advisors identify at-risk clients and provides individuals with personalized budgeting benchmarks.",
        "lessons": [
            "Data quality challenges in self-reported surveys",
            "Interpretability trade-offs in financial ML models",
            "Value of simple visualizations for non-technical stakeholders"
        ],
        "future_improvements": [
            "Integration with banking APIs for real data",
            "Mobile app with personalized recommendations",
            "Longitudinal tracking of financial behavior"
        ],
        "github_link": "#",
        "live_link": "#",
        "report_link": "#"
    },
    'dance-academy': {
        "title": "JC Dance Academy Website With User Friendly Interface",
        "category": "Web Development",
        "main_image": "images/dance-thumbnail.png",
        "date": "Jan 2024 - Mar 2024",
        "duration": "2 months",
        "team_size": "Duo",
        "description": "Responsive website for a dance academy featuring class schedules, instructor profiles, and registration system.",
        "problem_statement": "The academy needed a modern online presence to showcase their programs and streamline student enrollment.",
        "metrics": [
            {"value": "100%", "label": "Mobile Responsive"},
            {"value": "1.2s", "label": "Avg Load Time"},
            {"value": "5", "label": "Interactive Sections"},
            {"value": "300+", "label": "Monthly Visitors"}
        ],
        "technologies": ["HTML5", "CSS3", "JavaScript", "Swiper.js", "Font Awesome", "Git"],
        "solution": "Designed and developed a visually appealing, performance-optimized website with intuitive navigation.",
        "methodology": [
            "Conducted stakeholder interviews to identify requirements",
            "Created mobile-first responsive design",
            "Implemented Swiper.js for interactive galleries",
            "Optimized assets for fast loading",
            "Deployed with continuous integration"
        ],
        "challenges": [
            {
                "challenge": "Creating engaging animations without performance hits",
                "solution": "Used CSS transforms and hardware acceleration"
            },
            {
                "challenge": "Cross-browser compatibility",
                "solution": "Progressive enhancement and feature detection"
            }
        ],
        "visuals": [
            {"image": "images/dance-1.png", "caption": "Homepage hero slider"},
            {"image": "images/dance-2.png", "caption": "Class schedule section"},
            {"image": "images/dance-3.png", "caption": "Mobile responsive design"},
            {"image": "images/dance-4.png", "caption": "Registration form"}
        ],
        "outcomes": [
            "Increased class sign-ups by 35%",
            "Reduced admin workload with online registration",
            "Improved brand perception with modern design",
            "Achieved perfect Lighthouse accessibility score"
        ],
        "impact": "The website became the primary marketing channel, replacing printed brochures and reducing customer acquisition costs by 60%.",
        "lessons": [
            "Importance of UX in conversion optimization",
            "Balancing aesthetics with performance",
            "Client communication in iterative design"
        ],
        "future_improvements": [
            "Integration with payment gateways",
            "Student portal with progress tracking",
            "Video content delivery system"
        ],
        "github_link": "#",
        "live_link": "#",
        "report_link": "#"
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')

@app.route('/projects')
def show_projects():
    return render_template('projects.html', projects=projects)

@app.route('/projects/<project_id>')
def project_detail(project_id):
    project = projects.get(project_id)
    if not project:
        abort(404)
    return render_template('project_detail.html', project=project)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']
            
            # Send email to yourself
            msg = Message(
                subject=f"New message from {name}",
                recipients=[app.config['MAIL_USERNAME']],
                body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            )
            mail.send(msg)
            
            flash('Message sent successfully!', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            print(f"Error: {e}")
            flash('Failed to send message. Please try again later.', 'error')
            return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        # Get form data
        name = request.form['name']
        email = request.form['email']
        company = request.form.get('company', 'Not specified')
        opportunity = request.form['opportunity']
        message_content = request.form['message']
        
        # 1. Send HTML email to yourself
        msg_to_you = Message(
            subject=f"New Contact: {name} - {opportunity}",
            recipients=[app.config['MAIL_USERNAME']]
        )
        msg_to_you.html = render_template(
            "emails/admin_notification.html",
            name=name,
            email=email,
            company=company,
            opportunity=opportunity,
            message=message_content
        )
        mail.send(msg_to_you)
        
        # 2. Send HTML confirmation to user
        msg_to_user = Message(
            subject="Thanks for contacting me!",
            recipients=[email]
        )
        msg_to_user.html = render_template(
            "emails/user_confirmation.html",
            name=name,
            opportunity=opportunity,
            message=message_content
        )
        mail.send(msg_to_user)
        
        flash('Message sent successfully! Check your email for confirmation.', 'success')
        return redirect(url_for('contact'))
        
    except Exception as e:
        print(f"Email error: {str(e)}")
        flash('Failed to send message. Please try again later.', 'error')
        return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True)