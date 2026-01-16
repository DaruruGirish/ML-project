"""
Utility script to seed initial resources into the database.
"""
from backend.models import db, Resource

def seed_resources():
    """Seed initial mental health resources"""
    
    resources = [
        # Blogs
        {
            'title': '10 Science-Backed Ways to Reduce Stress',
            'description': 'Evidence-based techniques including deep breathing, meditation, and exercise.',
            'resource_type': 'blog',
            'category': 'research',
            'url': 'https://www.healthline.com/health/stress-relief',
            'source': 'Healthline',
            'icon_name': 'Brain',
            'image_url': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&h=400&fit=crop',
            'read_time_minutes': 8,
            'tags': ['Research', 'Lifestyle'],
            'is_featured': True
        },
        {
            'title': 'The Art of Mindful Living',
            'description': 'Learn how to practice mindfulness in your daily activities for lasting calm.',
            'resource_type': 'blog',
            'category': 'mindfulness',
            'url': 'https://www.mindful.org/',
            'source': 'Mindful.org',
            'icon_name': 'Leaf',
            'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400&fit=crop',
            'read_time_minutes': 6,
            'tags': ['Mindfulness', 'Practice'],
            'is_featured': True
        },
        {
            'title': 'Understanding the Stress Response',
            'description': 'How your body reacts to stress and what you can do to manage it effectively.',
            'resource_type': 'blog',
            'category': 'health',
            'url': 'https://www.health.harvard.edu/stress',
            'source': 'Harvard Health',
            'icon_name': 'Heart',
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=400&fit=crop',
            'read_time_minutes': 10,
            'tags': ['Science', 'Health'],
            'is_featured': True
        },
        {
            'title': 'Building Resilience Against Stress',
            'description': 'Develop mental strength and coping strategies for life\'s challenges.',
            'resource_type': 'blog',
            'category': 'growth',
            'url': 'https://www.psychologytoday.com/us/basics/resilience',
            'source': 'Psychology Today',
            'icon_name': 'Sparkles',
            'image_url': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&h=400&fit=crop',
            'read_time_minutes': 7,
            'tags': ['Psychology', 'Growth'],
            'is_featured': True
        },
        
        # Wikipedia Articles
        {
            'title': 'Stress Management',
            'description': 'Comprehensive overview of techniques and strategies for managing stress in daily life.',
            'resource_type': 'wikipedia',
            'category': 'education',
            'url': 'https://en.wikipedia.org/wiki/Stress_management',
            'source': 'Wikipedia',
            'icon_name': 'Brain',
            'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=400&fit=crop',
            'read_time_minutes': 10,
            'tags': ['Education', 'Overview'],
            'is_featured': False
        },
        {
            'title': 'Relaxation Technique',
            'description': 'Various methods used to reduce stress, anxiety, and produce a state of calm.',
            'resource_type': 'wikipedia',
            'category': 'practice',
            'url': 'https://en.wikipedia.org/wiki/Relaxation_technique',
            'source': 'Wikipedia',
            'icon_name': 'Waves',
            'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=400&fit=crop',
            'read_time_minutes': 8,
            'tags': ['Practice', 'Techniques'],
            'is_featured': False
        },
        {
            'title': 'Meditation',
            'description': 'Practice of focused attention to achieve mental clarity and emotional calmness.',
            'resource_type': 'wikipedia',
            'category': 'mindfulness',
            'url': 'https://en.wikipedia.org/wiki/Meditation',
            'source': 'Wikipedia',
            'icon_name': 'Leaf',
            'image_url': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&h=400&fit=crop',
            'read_time_minutes': 12,
            'tags': ['Mindfulness', 'Practice'],
            'is_featured': False
        },
        {
            'title': 'Progressive Muscle Relaxation',
            'description': 'Technique involving tensing and relaxing muscle groups to reduce physical tension.',
            'resource_type': 'wikipedia',
            'category': 'practice',
            'url': 'https://en.wikipedia.org/wiki/Progressive_muscle_relaxation',
            'source': 'Wikipedia',
            'icon_name': 'Activity',
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=400&fit=crop',
            'read_time_minutes': 6,
            'tags': ['Practice', 'Techniques'],
            'is_featured': False
        },
        
        # Resources
        {
            'title': 'Guided Meditations',
            'description': 'Curated collection of free guided meditation sessions for beginners and experienced practitioners.',
            'resource_type': 'meditation',
            'category': 'audio',
            'url': 'https://www.headspace.com/meditation/guided-meditation',
            'source': 'Headspace',
            'icon_name': 'Headphones',
            'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400&fit=crop',
            'read_time_minutes': None,
            'tags': ['Audio', 'Meditation'],
            'is_featured': True
        },
        {
            'title': 'Journaling Prompts',
            'description': 'Thoughtful prompts to help you process emotions and reflect on your mental state.',
            'resource_type': 'journaling',
            'category': 'writing',
            'url': 'https://www.verywellmind.com/journaling-prompts-for-stress-relief-3144671',
            'source': 'Verywell Mind',
            'icon_name': 'PenTool',
            'image_url': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800&h=400&fit=crop',
            'read_time_minutes': None,
            'tags': ['Writing', 'Reflection'],
            'is_featured': True
        },
        {
            'title': 'Breathing Exercises',
            'description': 'Step-by-step breathing techniques including 4-7-8, box breathing, and more.',
            'resource_type': 'breathing',
            'category': 'practice',
            'url': 'https://www.healthline.com/health/breathing-exercise',
            'source': 'Healthline',
            'icon_name': 'Wind',
            'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=400&fit=crop',
            'read_time_minutes': None,
            'tags': ['Practice', 'Breathing'],
            'is_featured': True
        },
        {
            'title': 'Professional Help Directory',
            'description': 'Directory of mental health resources, hotlines, and professional support services.',
            'resource_type': 'support',
            'category': 'support',
            'url': 'https://www.mentalhealth.gov/get-help',
            'source': 'MentalHealth.gov',
            'icon_name': 'Heart',
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=400&fit=crop',
            'read_time_minutes': None,
            'tags': ['Support', 'Professional'],
            'is_featured': True
        },
    ]
    
    for resource_data in resources:
        # Check if resource already exists
        existing = Resource.query.filter_by(
            title=resource_data['title'],
            resource_type=resource_data['resource_type']
        ).first()
        
        if not existing:
            resource = Resource(**resource_data)
            db.session.add(resource)
            print(f"Added resource: {resource_data['title']}")
        else:
            print(f"Resource already exists: {resource_data['title']}")
    
    db.session.commit()
    print("Resources seeded successfully!")

if __name__ == '__main__':
    from backend import create_app
    app = create_app()
    with app.app_context():
        seed_resources()
