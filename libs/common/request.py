import json
import requests
from libs.common.log import logger
from libs.common.content_type import ContentType
from libs.utils.json_utils import JsonUtils
import datetime
import time


class ApiRequest:

    timeout = 300

    def __init__(self, url, method, body=None, json_body=None, verify=True):
        """
        init the request with the given parameters
        :param url: the request server url, can be the host/domain, including the path and params
        :param method: the request method, it should be "get, post, put, delete"
        :param body: the request body
        :param json_body: the request body and it is set to json format
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
        """
        self.url = url
        self.method = method
        self.data = body
        self.json_body = json_body
        self.headers = {}
        self.path = ""
        self.params = {}
        self.verify = verify
        self.files = []
        self.proxies = None
        self.url_params = []
        self.allow_redirects = True

    @classmethod
    def get(cls, url):
        """
        init the Http Get method
        :param url: the test host or whole url
        :return: object of ApiRequest
        """
        return cls(url, "get")

    @classmethod
    def post(cls, url):
        """
        init the Http Post method
        :param url: the test host or whole url
        :return: object of ApiRequest
        """
        return cls(url, "post")

    @classmethod
    def put(cls, url):
        """
        init the Http Put method
        :param url: the test host or whole url
        :return: object of ApiRequest
        """
        return cls(url, "put")

    @classmethod
    def delete(cls, url):
        """
        init the Http Delete method
        :param url: the test host or whole url
        :return: object of ApiRequest
        """
        return cls(url, "delete")

    def set_token(self, token):
        """
        Add authorization token for the API request
        :param token: the access token
        :return: the request itself
        """
        if token is not None:
            self.headers["Authorization"] = token
        return self

    def add_header(self, key, value):
        """
        Add special header for the API request
        :param key: the header key
        :param value: the value
        :return: the request itself
        """
        if value is not None:
            self.headers[key] = value
        return self

    def set_content_type(self, content_type=ContentType.APPLICATION_JSON):
        """
        set the content type of the body
        :param content_type: the content type of the body, the content_type should be instance of ContentType
        :return: the request itself
        """
        if isinstance(content_type, ContentType):
            content_type = content_type.value
        self.headers["Content-Type"] = content_type
        return self

    def add_path(self, path):
        """
        Add the api path to the to the url
        :param path: the api path
        :return: the request itself
        """
        self.path += "/" + str(path)
        return self

    def add_param(self, key, value):
        """
        add the parameter to request
        :param key: the variable name
        :param value: the value
        :return: the request itself
        """
        if value is not None:
            self.params[key] = value
        return self

    def add_params(self, key, values):
        """
        add the parameter to request
        :param key: the variable name
        :param values: the value
        :return: the request itself
        """
        if values is not None:
            self.params[key] = ",".join(values)
        return self

    def add_params_to_url(self,  key, values):
        """
        Request seems not support the params which has the same key, so we just put the param into the url
        :param key: the variable name
        :param values: the value list
        :return:
        """
        if values is not None:
            for value in values:
                self.url_params.append(key + "=" + value)
        return self

    def add_file(self, field, path):
        """  support file upload, and this should be set to files field
        :param field: the file's filed name
        :param path: the file's path
        :return: the request itself
        """
        if path is not None:
            self.files.append((field, open(path, "rb")))
        return self

    def set_body(self, body, auto_config=True):
        """
        input the request body, it can be json, string, or class object
        :param body: the request body
        :param auto_config: if true, will automated to check the type of the body
        :return: the request itself
        """
        if body is None:
            return self

        if not auto_config:
            self.data = body
            return self

        if JsonUtils.is_json(body) or isinstance(body, dict) or isinstance(body, list):
            self.set_json(body)
        elif isinstance(body, str):
            self.data = body
        else:
            self.set_json(JsonUtils.object_to_json(body))
        return self

    def set_json(self, json):
        """
        set the request body and the body should be json, it will format the json
        and set the content_type to "application/json" by itself, so that we don't need to set again
        :param json: the json body
        :return: the request itself
        """
        if json is not None:
            self.json_body = json
        return self

    def is_verify(self, is_verify):
        """
        :param is_verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
        :return:
        """
        self.verify = is_verify
        return self

    def add_proxy(self, proxy_http, proxy_ip):
        """
        add proxy to the request
        :param proxy_http: the api proxy, http or https
        :param proxy_ip: the api proxy ip
        :return: the request itself
        """
        if self.proxies is None:
            self.proxies = {}
        self.proxies[proxy_http] = proxy_ip
        return self

    def is_redirect(self, allow_redirects=False):
        """
        most time, the request is automated redirect, but sometimes, in order to get the in-progress status,
        we need to block the redirect
        :param allow_redirects: default is False
        :return:
        """
        self.allow_redirects = allow_redirects
        return self

    def send(self):
        """
        Assemble the request and send it to the server. get the response
        :return: the object of ApiResponse
        """

        if len(self.url_params) > 0:
            self.path = "?" + "&".join(self.url_params)

        # set the path to the url
        if self.url[-1] == "/":
            self.url = self.url[:-1]
        if self.path != "":
            self.url = self.url + self.path

        # add a tag for automation test request
        self.params["test"] = "automation"

        logger.info("=" * 150)

        self.__print_request()
        current = time.time()
        r = requests.request(self.method, self.url, params=self.params, data=self.data, files=self.files,
                             json=self.json_body, headers=self.headers, verify=self.verify, timeout=self.timeout,
                             proxies=self.proxies, allow_redirects=self.allow_redirects)

        logger.info("=== time cost:       " + str((time.time() - current) * 1000))

        api_response = ApiResponse(r)
        api_response.print_response()

        return api_response

    def __print_request(self):
        """
        this is a private method just logging the request info
        :return:
        """
        logger.info("==> current time: " + datetime.datetime.now().strftime('%F %H:%M:%S.%f'))
        logger.info("==> request:")
        logger.info("==> " + self.method + " : " + self.url)
        if self.params != {}:
            logger.info("==> params: ")
            for key, value in self.params.items():
                logger.info("==>   " + key + " : " + str(value))
        if self.headers != {}:
            logger.info("==> headers: ")
            for i in JsonUtils.dict_generator(self.headers):
                logger.info("==>   " + json.dumps(i))
        if len(self.files) > 0 :
            logger.info("==> files: ")
            for file in self.files:
                logger.info("==>   " + str(file))
        if self.data is not None:
            logger.info("==> payload:")
            logger.info("==>   " + str(self.data))
        if self.json_body != {} and self.json_body is not None:
            logger.info("==> payload:")
            logger.info("==>   " + json.dumps(self.json_body, ensure_ascii=False, indent=4))
        logger.info("==>")


class ApiResponse:

    def __init__(self, response):
        self.status = response.status_code
        self.headers = response.headers
        self.url = response.url
        self.encoding = response.encoding
        self.text = response.text
        self.json = response.json
        self.elapsed = response.elapsed
        self.content = response.content

    def assert_status(self, status):
        """
        Assert the response status code should be the expected code
        :param status: int value, the http status code, such as 2XX, 3XX, 4XX, 5XX and so on.
        :return: the response itself
        """
        assert self.status == status, "Expected the response status is "\
                                      + str(status) + ", but actually is " + str(self.status)
        return self

    def assert_content_type(self, content_type=ContentType.APPLICATION_JSON):
        """
        Assert the response body's content type
        :param content_type: instance of ContentType, default is ContentType.APPLICATION_JSON
        :return: the response itself
        """
        if isinstance(content_type, ContentType):
            content_type = content_type.value
        assert content_type in self.headers["Content-Type"], \
            "Expected the content type of the body is: "\
            + content_type + ", but actually is: " + self.headers["Content-Type"]
        return self

    def assert_header(self, key, value, is_strict=False):
        """
        Assert the response body's content type
        :param key: the header's key which to be checked
        :param value: the expected value
        :param is_strict: if True, strictly compare the value
        :return: the response itself
        """
        if is_strict:
            assert value == self.headers[key], \
                "Expected the header: " + key + " , value: " + value + ", but actually value is " + self.headers[key]
        else:
            assert value in self.headers[key], \
                "For header " + key + ", expected " + value + " in " + self.headers[key] + " , but actually not"

        return self

    def assert_body(self, json_body=None, contain_str=None, xml_body=None, is_expected=True,
                    ignore_order=False, ignore_string_case=False, exclude_paths=None):
        """
        Verify the response body according to the given values
        :param json_body: the expected response body, it should be a json ar dict
        :param contain_str:  a string parameter, which will be checked whether it is a substring of the response body or not.
        :param xml_body: TODO: the xml format body. Because most of the APIs are using json format now, we just finished
         the json validation methon at the moment. once there is the requirement to check xml body, we will add the xml validation flows
        :param is_expected: this parameter should work with parameter contain_str. default is true, the response should
         contain expected values. if is_expected is False, verify the response not contains the input strings
        :return: ApiResopnse itself
        """
        if not is_expected:
            assert str(contain_str) not in self.text, "Checking the expected string: \"" + str(contain_str) + \
                                             "\" not in the response body, but it is existed. body >>>\n " + self.text
        else:
            if contain_str is not None:
                assert str(contain_str) in self.text, "Failed to find the expected string: \"" + str(contain_str) + \
                                                 "\" in the response body >>>\n " + self.text
            elif json_body is not None:
                if not (isinstance(json_body, str) or isinstance(json_body, dict) or isinstance(json_body, list)):
                    json_body = JsonUtils.object_to_json(json_body)
                JsonUtils.dict_compare(self.json(), json_body,
                                       ignore_order=ignore_order, ignore_string_case=ignore_string_case, exclude_paths=exclude_paths)

            elif xml_body is not None:
                # TODO: need to be implemented.
                raise NotImplementedError("XML validation is not implemented.")
            else:
                raise ValueError("Input parameter error!")

        return self

    def get_header(self, key):
        """
        return the special header value of the response
        :param key: the header's key
        :return:
        """
        return self.headers[key]

    def print_response(self):
        """
        this is a method just logger the request info
        :return:
        """
        logger.info("<== current time: " + datetime.datetime.now().strftime('%F %H:%M:%S.%f'))
        logger.info("<== response:")
        logger.info("<== elapsed: " + str(self.elapsed))
        logger.info("<== Status: " + str(self.status))
        if self.headers != {}:
            logger.info("<== headers:")
            for i in JsonUtils.dict_generator(self.headers):
                logger.info("<==   " + json.dumps(i))
        logger.info("<== payload:")
        try:
            logger.info("<==   " + json.dumps(json.loads(self.text), ensure_ascii=False, indent=4))
        except Exception:
            logger.info("<==   " + self.text)
        logger.info("<== request is done!\n")

