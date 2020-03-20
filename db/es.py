#coding: utf-8
import requests

ES_URL = "https://editor.rocketai.cn"

class EsOperate(object):
    """
    ES官方文档，最好的学习资料:
    https://www.elastic.co/guide/en/elasticsearch/reference/master/sql-overview.html
    """

    def __init__(self, url=ES_URL):
        self.url = url

    def query_by_one_item(self, index, condition):
        """
        通过一个条件来查询记录
        :param index: 表名
        :param condition:  Tuple 查询条件 示例:(k,v)
        :return: Dictionary
        """
        url = "{0}/{1}/_search".format(self.url, index)
        body = {
            "query": {
                "term": {
                    condition[0]: condition[1]
                }
            }
        }
        r = requests.get(url, json=body)
        if r.status_code == 200:
            result = r.json()
            if not result:
                return None
            if result['hits']['total']['value'] == 0:
                return None
            else:
                return result['hits']['hits'][0]['_source'] if result['hits']['hits'][0] else None

    def query_by_mutiple_item(self, index, condition, sort_codition=None, size_condition=None):
        """
        通过多个条件查询
        :param index:              String  表名
        :param condition:          Dictionary 查询条件
        :param sort_codition:      Dictionary 排序条件。示例:{'create_time': 'desc'}
        :param size_condition:     Dictionary 指定大小。示例:{'from'：0, 'size':1}  如果没有指定大小，es默认返回前10条
        :return:                   List<Dictionary>
        """
        url = "{0}/{1}/_search".format(self.url, index)
        body = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }
        for (k, v) in condition.iteritems():
            body['query']['bool']['must'].append({
                "match": {
                    k: v
                }
            })
        if sort_codition:
            body['sort'] = []
            for (k, v) in sort_codition.iteritems():
                body['sort'].append({k: v})
        if size_condition:
            body['from'] = size_condition['from']
            body['size'] = size_condition['size']

        r = requests.get(url, json=body)
        if r.status_code == 200:
            result = r.json()
            datas = result['hits']['hits']
            return map(lambda data:data['_source'], datas)
        else:
            return []

    def update_by_query(self, index, update_obj, query_obj):
        """
        对查询到的结果进行更新
        :param index:          String       表名
        :param update_obj:     Dictionary   待更新的字段
        :param query_obj:      Dictionary   查询条件
        :return:               Integer      受影响的行数
        """
        url = "{0}/{1}/_update_by_query".format(self.url, index)
        body = {
             "script": {},
             "query": {
                "bool": {
                    "must": []
                }
            }
        }
        for (k, v) in query_obj.iteritems():
            body['query']['bool']['must'].append({
                "match": {
                    k: v
                }
            })
        s = ""
        for (k, v) in update_obj.iteritems():
            s += "ctx._source['%s']='%s';" % (k, v)
        body['script'] = {'source': s}

        r = requests.post(url, json=body)
        if r.status_code == 200:
            result = r.json()
            return result.get('updated', 0)
        else:
            return 0

    def insert(self, index, obj):
        """
        插入新记录
        :param index:  String  表名
        :param obj:    Dictionary  带插入的对象
        :return:       Integer  成功的条数
        """
        url = "{0}/{1}/_doc".format(self.url, index)
        r = requests.post(url, json=obj)
        # 201: created
        if r.status_code == 200 or r.status_code == 201:
            result = r.json()
            return result['_shards']['successful']
        else:
            return 0

    def create_index_mapping(self, index, mapping):
        """
        建立表结构。表结构字段一旦建立就不能修改类型了。如需修改类型，可以参考官方文档:
        https://www.elastic.co/guide/en/elasticsearch/reference/master/mapping.html Update the mapping of a field
        keyword不分词，text分词.
        keyword可以分组，text不能分组。
        es数据类型有: text,keyword,date,long,double,boolean,integer,object
        :param index:      String  表名
        :param mapping:    Dictionary 指名字段类型的字典 example: {"title": ""}
        :return:
        """

        url = "{0}/{1}".format(self.url, index)
        body = {
            "mappings": {
                "properties": {}
            }
        }
        for (k, v) in mapping.items():
            body['mappings']['properties'][k] = {'type': v}

        r = requests.put(url, json=body)
        # 201: created
        if r.status_code == 200 or r.status_code == 201:
            result = r.json()
            return result['acknowledged']
        else:
            return False

    def add_new_field_to_index(self, index, mapping):
        """
        往index中新增新的字段。
        :param index:    String   表名
        :param mapping:  Dictionary  待新增的字段
        :return:         Boolean
        """
        url = "{0}/{1}/_mapping".format(self.url, index)
        body = {
            "properties": {}
        }
        for (k, v) in mapping.items():
            body['properties'][k] = {'type': v}

        r = requests.put(url, json=body)
        # 201: created
        if r.status_code == 200 or r.status_code == 201:
            result = r.json()
            return result['acknowledged']
        else:
            return False


    def query_by_time(self, index, time_field, start_time, end_time):
        """
        根据时间范围查询数据
        :param index:          String  表名
        :param time_field:     String  时间字段
        :param start_time:     String  开始时间
        :param end_time:       String  结束时间
        :return:               List<Dictionary>
        """
        body = {
            "query": {
                "range": {
                    time_field: {
                        "gte": start_time,
                        "lt": end_time
                    }
                }
            }
        }
        url = "{0}/{1}/_search".format(self.url, index)
        r = requests.get(url, json=body)
        if r.status_code == 200:
            result = r.json()
            datas = result['hits']['hits']
            return map(lambda data: data['_source'], datas)
        else:
            return []

    def query_field_aggregation_result(self, index, field):
        """
        查询某个字段的分组结果
        :param index:  String   表名
        :param field:  String   某字段
        :return:       List<Dictionary>
        """
        url = "{0}/{1}/_search".format(self.url, index)
        body = {
            "size": 0,
            "aggs": {
                "source_term": {
                    "terms": {
                        "field": field,
                        "size": 10000  #默认es返回10条，所以把值设大点返回全部
                    }
                }
            }
        }
        r = requests.get(url, json=body)
        if r.status_code == 200:
            result = r.json()
            if result:
                return result['aggregations']['source_term']['buckets']
            else:
                return []
        else:
            return []

    def del_index(self, index):
        """
        删除整张表
        :param index: String 表名
        :return:      Boolean
        """
        url = "{0}/{1}".format(self.url, index)

        r = requests.delete(url)
        if r.status_code == 200:
            return r.json()['acknowledged']
        else:
            return False



if __name__ == '__main__':
    es_operate = EsOperate()
    # print es_operate.query_by_one_item('fangan', ('test', 'test1'))
    # print es_operate.query_by_mutiple_item('cp_req',
    #                                        {'phone': '18938881156', 'sex': '男'},
    #                                        {"create_time": "desc"},
    #                                        {'from':0, 'size':1})
    # print es_operate.update_by_query('fangan', {'cuserId': '', 'customerId': ''}, {'_id': 'nTOlb28BESWuSQOZb3nI'})
    # print change_dic_to_json_str(es_operate.query_field_aggregation_result('craw_data', 'content'))
    # print change_dic_to_json_str(es_operate.query_by_mutiple_item('intel_fangan', {'sex': '男'}, size_condition={'from':0, 'size':10000}))
    # print es_operate.query_field_aggregation_result('fangan', 'age')
    print(es_operate.del_index('intel_fangan'))
    # print es_operate.create_index_mapping('intel_fangan', {
    #     'age': 'keyword'
    # })
    # print es_operate.add_new_field_to_index("intel_fangan", {'age5': 'object'})