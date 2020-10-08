class RequestValidatorService:
    @staticmethod
    def validate_query_params(agrs):
        required = ['date_from', 'date_to', 'origin', 'destination']
        values = []
        for param in required:
            if not agrs.get(param):
                return False
            else:
                values.append(agrs.get(param))
        return values
    
    @staticmethod
    def validate_body_params(args):
        required = ['date_from', 'date_to', 'origin_code', 'destination_code', 'price', 'currency']
        values = []
        for param in required:
            if param not in args:
                return False
            else:
                values.append(args[param])
        return values