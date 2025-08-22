# RE/MAX Backend API

A Django REST API backend for RE/MAX property management system with news, testimonials, and property inquiry features.

## Features

- **Property Management**: CRUD operations for properties and categories
- **News System**: News articles with auto-generated slugs
- **Testimonials**: Customer testimonials with ratings
- **Property Inquiries**: Customer inquiries for properties
- **Property Search**: Advanced filtering with location-based search
- **Image Upload**: Support for property and news images

## Tech Stack

- **Django 5.2.5**
- **Django REST Framework 3.16.1**
- **SQLite** (Development)
- **Pillow** (Image processing)
- **CORS Headers** (Cross-origin requests)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/muhzee733/remax-backend.git
   cd remax-backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Properties

- `GET/POST /api/v1/property/` - List/Create properties
- `GET/PUT/PATCH/DELETE /api/v1/property/{slug}/` - Property CRUD by slug
- `GET /api/v1/find-property/?location=required&other=optional` - Search properties
- `GET /api/v1/property-categories/` - List property categories
- `GET /api/v1/category/{slug}/properties/` - Properties by category

### News

- `GET/POST /api/v1/news/` - List/Create news articles
- `GET /api/v1/news/{slug}/` - Get news by slug
- `GET /api/v1/news/{slug}/related/` - Get related news

### Testimonials

- `GET/POST /api/v1/testimonial/` - List/Create testimonials

### Property Inquiries

- `GET/POST /api/v1/inquiry/` - List/Create property inquiries

## API Examples

### Create News Article
```bash
curl -X POST http://127.0.0.1:8000/api/v1/news/ \
  -F "title=Market Update: Q1" \
  -F "desc=Dubai real estate shows strong growth." \
  -F "date=2025-01-15" \
  -F "image=@path/to/image.jpg"
```

### Search Properties
```bash
curl "http://127.0.0.1:8000/api/v1/find-property/?location=Dubai%20Islands&propertyType=Apartment&bedroom=1&bathroom=2"
```

### Create Property Inquiry
```bash
curl -X POST http://127.0.0.1:8000/api/v1/inquiry/ \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": 2,
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+971501234567",
    "message": "I am interested in this property"
  }'
```

### Create Testimonial
```bash
curl -X POST http://127.0.0.1:8000/api/v1/testimonial/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah M.",
    "rating": 5,
    "text": "I recently bought my first home through RE/MAX and the process was smooth from start to finish."
  }'
```

## Models

### Property
- Category (ForeignKey)
- Property details (name, description, location)
- Pricing and specifications
- Image gallery
- JSON fields for search filters
- Auto-generated slug

### News
- Title, description, date
- Image upload
- Auto-generated slug
- Related news functionality

### Testimonial
- Name, rating (1-5), text
- Auto timestamp

### PropertyInquiry
- Property reference
- Customer details (name, email, phone)
- Message
- Auto timestamp

## Admin Interface

Access the Django admin at `/admin/` to manage:
- Properties and categories
- News articles
- Testimonials
- Property inquiries

## Development

### Project Structure
```
property/
├── property/          # Main Django project
├── propertyCrud/      # Property management app
├── news/             # News articles app
├── testimonial/      # Testimonials app
├── inquiry/          # Property inquiries app
├── media/            # Uploaded files
└── manage.py
```

### Key Features
- **Auto-slug generation** for SEO-friendly URLs
- **Image upload** support for properties and news
- **Advanced property search** with multiple filters
- **CORS enabled** for frontend integration
- **Comprehensive validation** for all inputs

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request
