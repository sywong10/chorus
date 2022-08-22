from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from flask_cors import CORS
from models import setup_db, db, Singer, Choir, ChoirEnrollment
from auth import AuthError, requires_auth

NUMBER_PER_PAGE = 10

def pagination(request, selection):
    # print(type(selection))
    # print(selection[0].name)
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * NUMBER_PER_PAGE
    end = page * NUMBER_PER_PAGE
    # singers = [s.long() for s in selection]
    current_singers = selection[start:end]
    # current_singers = singers[start:end]
    return current_singers


def sort_by_voice_part(singers):
    SOPRANO = []
    ALTO = []
    TENOR = []
    BASS = []

    for i in singers:
        if i.voice_part == 'soprano':
            SOPRANO.append(i.name)
        elif i.voice_part == 'alto':
            ALTO.append(i.name)
        elif i.voice_part == 'tenor':
            TENOR.append(i.name)
        elif i.voice_part == 'bass':
            BASS.append(i.name)

    return(SOPRANO, ALTO, TENOR, BASS)


def create_app(test_config=None):
    # print(__name__)
    app = Flask(__name__)
    migrate = Migrate(app, db)

    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE')
        return response


    @app.route('/')
    def index():
        return 'Chorus app'


    @app.route('/singers', methods=['GET'])
    @requires_auth('get:singers')
    def get_paginated_singers(jwt):

        selection = Singer.query.all()
        current_selection = pagination(request, selection)
        singers = [s.long() for s in current_selection]

        if len(singers) > 0:
            return jsonify({
                'success': True,
                'singers': singers,
                'total singers': len(selection)
            }), 200
        else:
            abort(404)


    @app.route('/singers/<int:singer_id>', methods=['GET'])
    @requires_auth('get:singers')
    def get_specific_singer(jwt, singer_id):

        singer = Singer.query.filter(Singer.id == singer_id).one_or_none()

        if singer:
            return jsonify({
                'success': True,
                'singer': singer.long()
            }), 200
        else:
            abort(404)



    @app.route('/singers', methods=['POST'])
    @requires_auth('post:singers')
    def add_singers(jwt):
        body = request.get_json()
        parts = ['soprano', 'alto', 'tenor', 'bass']

        new_name = body.get('name', None)
        new_phone = body.get('phone', None)
        new_voice_part = body.get('voice_part', None)
        new_not_available = body.get('not_available', None)

        check_new_singer = Singer.query.filter(Singer.name.ilike('%' + new_name + '%')).first()

        # should fail if singer already exists in singer table
        if check_new_singer:
            abort(409)

        # should fail if void part submitted is not supported
        if not new_voice_part in parts:
            abort(422)

        try:
            new_singer = Singer(
                name = new_name,
                phone = new_phone,
                voice_part = new_voice_part,
                not_available = new_not_available
            )

            new_singer.insert()

            return jsonify({
              'success': True,
              'singer added': new_name + ' added'
            }), 200

        except Exception as e:
            print(e)
            abort(422)



    # get list of singer in specified voice part
    # return of this function does not take enrollment into consideration


    @app.route('/singers/<voice_part>', methods=['GET'])
    @requires_auth('get:singers')
    def get_voice_type(jwt, voice_part):

        parts = ['soprano', 'alto', 'tenor', 'bass']

        if not voice_part in parts:
            abort(422)
        else:
            selection = Singer.query.filter(Singer.voice_part == voice_part).all()
            current_selection = pagination(request, selection)
            singers = [s.name for s in current_selection]

            return jsonify({
                'success': True,
                'total': len(selection),
                voice_part: singers
            })




    @app.route('/singers/<int:id>', methods=['PATCH'])
    @requires_auth('patch:singers')
    def modify_singer(jwt, id):
        body = request.get_json()
        updated_singer = Singer.query.filter(Singer.id==id).one_or_none()

        if updated_singer is None:
            abort(404)
        else:
            if not body.get("name", None) is None:
                updated_singer.name = body.get("name")

            if not body.get("phone", None) is None:
                updated_singer.phone = body.get("phone")

            if not body.get("voice_part", None) is None:
                updated_singer.voice_part = body.get("voice_part")

            if not body.get("not_available", None) is None:
                updated_singer.not_available = body.get("not_available")

            updated_singer.update()

            return jsonify({
                'success': True,
                'singer': updated_singer.long()
            }), 200





    @app.route('/singers/<int:id>', methods=['DELETE'])
    @requires_auth('delete:singers')
    def delete_singer(jwt, id):
        unenroll_singer = ChoirEnrollment.query.filter(ChoirEnrollment.singer_id==id).one_or_none()
        delete_singer = Singer.query.filter(Singer.id==id).one_or_none()

        if not delete_singer:
            abort(404)


        try:
            if not unenroll_singer:
                # print('this singer is not enrolled,  proceed to delete from singer table')
                delete_singer.delete()
            else:
                # print('the singer is enrolled, need to unenroll first, then delete from singer table')
                unenroll_singer.unenroll()
                delete_singer.delete()

            return jsonify({
                'success': True,
                'deleted singer': delete_singer.short()
            })

        except Exception as e:
            print(e)
            abort(422)




    @app.route('/choirs', methods=['GET'])
    @requires_auth('get:choirs')
    def get_choirs(jwt):

        try:
            choirs = Choir.query.all()

            return jsonify({
                'success': True,
                'choirs': [ choir.long() for choir in choirs ]
            }), 200

        except Exception as e:
            abort(422)



    @app.route('/choirs', methods=['POST'])
    @requires_auth('post:choirs')
    def add_choir(jwt):

        body = request.get_json()
        new_name = body.get("name", None)
        new_practice_time = body.get("practice_time", None)

        check_new_choir = Choir.query.filter(Choir.name.ilike('%' + new_name + '%')).first()

        if check_new_choir:
            abort(409)

        try:
            new_choir = Choir(
                name = new_name,
                practice_time = new_practice_time
            )

            new_choir.insert()

            return jsonify({
                'success': True,
                'choir added': new_choir.name
            })

        except Exception as e:
            print(e)
            abort(422)


    @app.route('/choirs/<int:id>', methods=['PATCH'])
    @requires_auth('patch:choirs')
    def update_choir(jwt, id):
        body = request.get_json()
        updated_choir = Choir.query.filter(Choir.id==id).one_or_none()

        if updated_choir is None:
            abort(404)

        try:
            if not body.get("name", None) is None:
                updated_choir.name=body.get("name")

            if not body.get("practice_time", None) is None:
                updated_choir.practice_time=body.get("practice_time")

            updated_choir.update()

            return jsonify({
                'success': True,
                'updated choir': updated_choir.long()
            }), 200

        except Exception as e:
            print(e)
            abort(422)





    @app.route('/choirs/<int:id>', methods=['DELETE'])
    @requires_auth('delete:choirs')
    def delete_choir(jwt, id):

        delete_choir = Choir.query.filter(Choir.id==id).one_or_none()

        if not delete_choir:
            abort(404)
        else:
            delete_choir.delete()
            return jsonify({
                'success': True,
                'removed choir': delete_choir.long()
            }), 200






    @app.route('/choir/<int:cid>', methods=['GET'])
    @requires_auth('get:choirs')
    def list_singers_in_choir(jwt, cid):

        selected_choir = Choir.query.filter(Choir.id == cid).one_or_none()
        singers = Singer.query.with_entities(Singer).join(ChoirEnrollment).filter(ChoirEnrollment.choir_id == cid).all()
        SOPRANO, ALTO, TENOR, BASS = sort_by_voice_part(singers)

        if not selected_choir:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'Choir name': selected_choir.name,
                'voice_type': {
                    'SOPRANO': (None, SOPRANO)[len(SOPRANO) > 0],
                    'ALTO': (None, SOPRANO)[len(ALTO) > 0],
                    'TENOR': (None, TENOR)[len(TENOR) > 0],
                    'BASS': (None, BASS)[len(BASS) > 0]
                }
            }), 200




    @app.route('/choir/<int:cid>/<s_voice_part>', methods=['GET'])
    @requires_auth('get:choirs')
    def choir_id_soprano(jwt, cid, s_voice_part):

        try:
            selected_choir = Choir.query.filter(Choir.id == cid).one_or_none()
            choir_part_result = Singer.query.with_entities(Singer).join(ChoirEnrollment).filter(
                ChoirEnrollment.choir_id == cid, Singer.voice_part == s_voice_part).all()

            return jsonify({
                'success': True,
                'Choir name': selected_choir.name,
                s_voice_part: [p.name for p in choir_part_result]
            }), 200

        except Exception as e:
            print(e)
            abort(404)




    @app.route('/enroll/<choir_name>/<int:sid>', methods=['POST'])
    @requires_auth('post:enroll_singer')
    def enroll_singer_to_choir(jwt, choir_name, sid):

        choir = Choir.query.filter(Choir.name.ilike('%' + choir_name + '%')).first()
        singer = Singer.query.filter(Singer.id == sid).one_or_none()

        if not singer:
            abort(404)

        if choir.practice_time.split(' ')[0].lower() in singer.not_available.lower():
            # print('there is a conflict')
            abort(409)

        else:
            # print('there is no conflict, good to go')
            enrollment = ChoirEnrollment(
                choir_id=choir.id,
                singer_id=singer.id,
            )

            enrollment.enroll()

            return jsonify({
            'success': True,
            'singer added': singer.name,
            'updated choir': choir.name,
            }), 200






    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable_entity"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(409)
    def schedule_conflict(error):
        return jsonify({
            "success": False,
            "error": 409,
            "message": "schedule conflict"
        }), 409


    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()

