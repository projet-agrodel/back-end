from flask import request, jsonify
from app.models.category import Category
from app.extensions import db
from app.utils.decorators import admin_required # Supondo que você tenha este decorador

class CategoryController:
    @staticmethod
    @admin_required()
    def get_all_categories():
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            categories_query = Category.query
            
            # Exemplo de filtro (pode ser expandido)
            search_term = request.args.get('search', type=str)
            if search_term:
                categories_query = categories_query.filter(Category.name.ilike(f'%{search_term}%'))

            categories_page = categories_query.order_by(Category.name.asc()).paginate(page=page, per_page=per_page, error_out=False)
            
            categories_list = [category.to_dict() for category in categories_page.items]
            
            # Adicionar productCount simulado se não estiver no to_dict real
            # Esta é uma simulação. O ideal é que to_dict() inclua a contagem real se necessário.
            for cat_dict in categories_list:
                if 'productCount' not in cat_dict:
                    cat_dict['productCount'] = db.session.query(db.func.count('*')).select_from(db.Table('products_categories', db.MetaData(), db.Column('category_id'))).filter_by(category_id=cat_dict['id']).scalar() or 0
                    # Ou, se você tiver um relacionamento direto Product.category_id:
                    # from app.models.product import Product # Evitar import circular
                    # cat_dict['productCount'] = Product.query.filter_by(category_id=cat_dict['id']).count()

            return jsonify({
                'message': 'Categorias recuperadas com sucesso.',
                'categories': categories_list,
                'total': categories_page.total,
                'pages': categories_page.pages,
                'current_page': categories_page.page,
                'per_page': categories_page.per_page
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @admin_required()
    def create_category():
        try:
            data = request.get_json()
            if not data or not data.get('name'):
                return jsonify({'error': 'Nome da categoria é obrigatório.'}), 400

            name = data['name']
            description = data.get('description')

            if Category.query.filter_by(name=name).first():
                return jsonify({'error': 'Uma categoria com este nome já existe.'}), 409 # Conflict

            new_category = Category(name=name, description=description)
            db.session.add(new_category)
            db.session.commit()
            
            # Simular productCount para a resposta, já que é um novo item
            category_dict = new_category.to_dict()
            if 'productCount' not in category_dict:
                 category_dict['productCount'] = 0

            return jsonify({
                'message': 'Categoria criada com sucesso.',
                'category': category_dict
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @admin_required()
    def get_category_by_id(category_id):
        try:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'error': 'Categoria não encontrada.'}), 404
            
            category_dict = category.to_dict()
            if 'productCount' not in category_dict:
                 from app.models.product import Product # Evitar import circular
                 category_dict['productCount'] = Product.query.filter_by(category_id=category_dict['id']).count()

            return jsonify({
                'message': 'Categoria recuperada com sucesso.',
                'category': category_dict
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @admin_required()
    def update_category(category_id):
        try:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'error': 'Categoria não encontrada.'}), 404

            data = request.get_json()
            if not data:
                return jsonify({'error': 'Nenhum dado fornecido para atualização.'}), 400

            if 'name' in data:
                new_name = data['name']
                if new_name != category.name and Category.query.filter_by(name=new_name).first():
                    return jsonify({'error': 'Uma categoria com este novo nome já existe.'}), 409
                category.name = new_name
            
            if 'description' in data:
                category.description = data['description']
            
            db.session.commit()

            category_dict = category.to_dict()
            # Simular productCount para a resposta
            if 'productCount' not in category_dict:
                 from app.models.product import Product # Evitar import circular
                 category_dict['productCount'] = Product.query.filter_by(category_id=category_dict['id']).count()

            return jsonify({
                'message': 'Categoria atualizada com sucesso.',
                'category': category_dict
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @admin_required()
    def delete_category(category_id):
        try:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'error': 'Categoria não encontrada.'}), 404
            
            # Adicionar verificação se a categoria está em uso por produtos
            # from app.models.product import Product 
            # if Product.query.filter_by(category_id=category_id).first():
            #     return jsonify({'error': 'Categoria está em uso por produtos e não pode ser excluída.'}), 409

            db.session.delete(category)
            db.session.commit()
            return jsonify({'message': 'Categoria excluída com sucesso.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500 