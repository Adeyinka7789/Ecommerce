
```markdown
#  ADM Ecommerce Site

Welcome to **Ecommerce Site**, a robust and user-friendly online store built with Django, designed to provide a seamless shopping experience. This platform combines a powerful backend with a modern, responsive frontend powered by JavaScript, HTML, CSS, and Tailwind CSS.

## 🚀 Overview

Ecommerce Site is a full-featured eCommerce platform for buying and selling fashion wares and other products. It offers secure user authentication, product management, cart functionality, and order tracking, with integration for Paystack payments. The site is optimized for small businesses and personal ventures, featuring a clean design and efficient workflows.

- **Purpose:** To create an online marketplace for excellent fashion wares and related products.
- **Target Audience:** Shoppers, small business owners, and developers.

## 🛠️ Technologies Used

- **Backend:** 
  - [Django](https://www.djangoproject.com/) - A high-level Python web framework (v5.2.1).
  - [Python](https://www.python.org/) - The core programming language.
  - [MySQL](https://www.mysql.com/) - Database engine for storing products, orders, and user data.
  - [django-db-logger](https://github.com/coderholic/django-db-logger) - For logging to the database.
  - [crispy_forms](https://django-crispy-forms.readthedocs.io/) with [crispy_bootstrap5](https://github.com/django-crispy-forms/crispy-bootstrap5) - For styled forms.
  - [widget_tweaks](https://github.com/jazzband/django-widget-tweaks) - For customizing form rendering.
- **Frontend:** 
  - [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) - For content structure.
  - [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) - Enhanced with [Tailwind CSS](https://tailwindcss.com/) for utility-first design.
  - [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - For interactive features.
- **Payment Integration:** [Paystack](https://paystack.com/) - For secure online transactions (configured via environment variables).

## 🌟 Features

- **Product Catalog:** Browse and filter products from the `products` app.
- **Shopping Cart:** Manage items in the cart via the `cart` app.
- **User Authentication:** Secure signup, login, and profile management with custom forms.
- **Order Management:** Track orders and view details in the `checkout` and `user_profile` sections.
- **Address Management:** Add, edit, and delete shipping addresses.
- **Wishlist:** Save favorite products using the `wishlist` app.
- **Analytics:** Monitor site usage with the `analytics` app.
- **Responsive Design:** Optimized for all devices using Tailwind CSS.
- **Contact Form:** Submit inquiries via the `core` app.
- **Payment Integration:** Process transactions with Paystack.

<img width="959" height="910" alt="mermaid-diagram-2025-10-17-162801" src="https://github.com/user-attachments/assets/b36db7a2-141f-48af-8b86-81a6cf2e429c" />

## 📋 Prerequisites

Before setting up the project, ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/) - Python package manager
- [Git](https://git-scm.com/) - For version control
- [MySQL Server](https://www.mysql.com/) - Database system
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (optional) - For isolated Python environments
- [python-decouple](https://github.com/henriquebastos/python-decouple) - For managing environment variables

## 🔧 Installation

Follow these steps to get the project running on your local machine:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/ecommerce-site.git
   cd ecommerce-site
   ```

2. **Create a Virtual Environment (Optional):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note:* Create `requirements.txt` with `pip freeze > requirements.txt` if not present.

4. **Set Up Environment Variables:**
   - Create a `.env` file in the project root and add:
     ```
     SECRET_KEY=your-secret-key-here
     DEBUG=True
     DATABASE_URL=mysql://root:Omowunmi77897789*@localhost:3306/ecomstore_db
     PAYSTACK_PUBLIC_KEY=your-paystack-public-key
     PAYSTACK_SECRET_KEY=your-paystack-secret-key
     ```
   - Generate a `SECRET_KEY` with `python -c "import secrets; print(secrets.token_urlsafe(50))"`.

5. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set up an admin account.

7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Visit `http://localhost:8000` to explore the store.

## 📝 Usage

- **Browse Products:** Navigate to `/products/` to view the catalog.
- **Add to Cart:** Use the cart functionality at `/cart/`.
- **Checkout:** Complete purchases at `/checkout/`.
- **Manage Account:** Sign up at `/accounts/signup/`, log in at `/accounts/login/`, and edit profiles at `/accounts/profile/`.
- **Track Orders:** View order history at `/accounts/orders/`.
- **Admin Panel:** Manage products and orders via `/admin/`.
- **Test Payments:** Configure Paystack keys to enable transactions.

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

Please follow the [Django Coding Style](https://docs.djangoproject.com/en/5.2/internals/contributing/writing-code/coding-style/).

## 🛡️ License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify it as per the license terms.

## 🙏 Acknowledgments

- Built with inspiration from the Django, Tailwind CSS, and Paystack communities.
- Thanks to contributors and users for their support.

## 📬 Contact

For questions or feedback, reach out to:
- **Email:** [Dotunm85@gmail.com](mailto:Dotunm85@gmail.com)
- **GitHub:** [your-username](https://github.com/your-username)

---

Happy selling with Ecommerce Site!
```


