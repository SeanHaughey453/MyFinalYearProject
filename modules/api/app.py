from datetime import timedelta
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from api.error_handling import ArangoException, DataModelException, GeneralException, InvalidCredentials, InvalidFormatException, ResourceConflictException, ResourceNotFoundException, UnauthorizedException

from api.schedule_api import Scedule_API, Scedule_API_API_Errors
from common.data_store_arango import DataStoreArangoDb
from pyArango.theExceptions import DocumentNotFoundError

from api.controller.auth.auth import Account, Login, Signup, StaffAccount, StaffAmmendClient, StaffAmmendClientsCredits, StaffAmmendClientsPlans, StaffAmmendCoWorker, StaffLogin, StaffSignup
from api.controller.resources.schedule import ModifyScheduleStaff, Schedules, Schedule
from api.controller.resources.booking_credit import BookingCredit
from api.controller.subresource.subresources import Booking
from api.controller.resources.plan import Plan

ARANGO_URL = os.environ.get('ARANGO_URL', 'http://localhost:8529')
ARANGO_DB_NAME = 'scheduleapp'
ARANGO_ACCOUNTS_DB_NAME = 'accounts'
ARANGO_COLLECTION_SCHEDULE = 'schedule'
ARRANGO_COLLECTION_STAFF = 'staff'
ARANGO_COLLECTION_USERS = 'users'
ARANGO_COLLECTION_BOOKING_CREDIT = 'booking_credit'
ARANGO_COLLECTION_PLAN = 'plan'
POSSIBLE_ERRORS = [[ArangoException, 400], [DataModelException, 400], [UnauthorizedException, 401], [GeneralException, 404], [ResourceNotFoundException, 404],
                    [DocumentNotFoundError, 404], [ResourceConflictException, 409], [InvalidCredentials, 409], [InvalidFormatException, 409]]
def create_app() -> Flask:

    errors = Scedule_API_API_Errors()

    #[errors.add_error(error[0], error[1]) for error in POSSIBLE_ERRORS]

    errors.add_error(GeneralException, 400)
    errors.add_error(ArangoException, 400)
    errors.add_error(DocumentNotFoundError, 404)
    errors.add_error(DataModelException, 400)
    errors.add_error(ResourceConflictException, 409)
    errors.add_error(ResourceNotFoundException, 404)
    errors.add_error(InvalidCredentials, 409)
    errors.add_error(InvalidFormatException, 400)
    errors.add_error(UnauthorizedException, 401)

    app = Flask('PythonApi')
    app.config['SECRET_KEY'] = 'super-secret-key'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)


    jwt = JWTManager(app)

    #open connections to arango collections at app start for simplicity
    app.data_store_schedules = DataStoreArangoDb(ARANGO_URL, ARANGO_DB_NAME, ARANGO_COLLECTION_SCHEDULE)
    app.data_store_users = DataStoreArangoDb(ARANGO_URL, ARANGO_ACCOUNTS_DB_NAME, ARANGO_COLLECTION_USERS)
    app.data_store_staff = DataStoreArangoDb(ARANGO_URL, ARANGO_ACCOUNTS_DB_NAME, ARRANGO_COLLECTION_STAFF)
    app.data_store_booking_credit = DataStoreArangoDb(ARANGO_URL, ARANGO_DB_NAME, ARANGO_COLLECTION_BOOKING_CREDIT)
    app.data_store_plan = DataStoreArangoDb(ARANGO_URL, ARANGO_DB_NAME, ARANGO_COLLECTION_PLAN)

    api = Scedule_API(error_list=errors, app=app) 


    baseScheduleUrl = '/v1/schedule'
    specificScheduleUrl = baseScheduleUrl + '/<scheduleId>'
    schedulesUrl = '/v1/schedules'

    baseCreditUrl = '/v1/credit'
    specificCreditURL = baseCreditUrl + '/<bookingCreditId>'
    creditsUrl = '/v1/credits'

    basePlanUrl = '/v1/plan'
    specificPlanUrl = basePlanUrl+ '/<planId>'

    #API
    #Client Auth
    api.add_resource(Signup, '/v1/signup')
    api.add_resource(Login, '/v1/login')
    api.add_resource(Account, '/v1/account/<username>', '/v1/account/edit/<username>', '/v1/account/delete/<username>')
    #Staff Auth
    api.add_resource(StaffSignup, '/v1/staff/signup')
    api.add_resource(StaffLogin, '/v1/staff/login')
    api.add_resource(StaffAccount, '/v1/staff/account/<username>', '/v1/staff/account/edit/<username>', '/v1/staff/account/delete/<username>')
    api.add_resource(StaffAmmendCoWorker, '/v1/staff/account/<username>/coworker/edit', '/v1/staff/account/<username>/coworker/delete')
    api.add_resource(StaffAmmendClient, '/v1/staff/account/<username>/client/edit', '/v1/staff/account/<username>/client/delete')
    api.add_resource(StaffAmmendClientsCredits, '/v1/credits/add/<clientId>/token/<bookingId>')
    api.add_resource(StaffAmmendClientsPlans, '/v1/plans/add/<clientId>/planid/<planId>')
    #Schedules
    api.add_resource(Schedules, schedulesUrl)
    api.add_resource(Schedule, baseScheduleUrl, specificScheduleUrl)
    api.add_resource(ModifyScheduleStaff, specificScheduleUrl+'/staff/add' )
    #booking
    api.add_resource(Booking, specificScheduleUrl+ '/<day>/<hour>')
    #booking credits
    api.add_resource(BookingCredit, baseCreditUrl,specificCreditURL)
    #plans
    api.add_resource(Plan, basePlanUrl, specificPlanUrl)


    return app