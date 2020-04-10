from TestUtils.models import BaseTestCase
from Achievements.models import Achievement


class LocalBaseTestCase(BaseTestCase):
    """
    Локальный базовый класс для тестов
    """
    def setUp(self):
        super().setUp()
        self.path = self.url_prefix + 'achievements/'
        self.user_token, self.moder_token, self.super_token, self.wrong_token = \
            'user', 'moderator', 'superuser', 'nea'
        self.ach = Achievement.objects.create(name='Name', descr='descr')


class AchievementsListTestCase(LocalBaseTestCase):
    """
    Тесты для спискового представления ачивок
    """
    def setUp(self):
        super().setUp()
        self.data_201 = {
            'name': 'Post',
        }
        self.data_400 = {

        }

    def testGet200_Ok(self):
        response = self.get_response_and_check_status(url=self.path, auth=False, token=self.user_token)
        self.fields_test(response, ['id', 'name', 'pic_id'])
        self.list_test(response, Achievement)

    def testGet200_Deleted(self):
        achd = Achievement.objects.create(name='Name', descr='descr', deleted_flg=True)
        response = self.get_response_and_check_status(url=self.path+'?with_deleted=True', auth=False)
        self.assertEqual(len(response), 2, msg='Deleted instances are not in response')

    def testPost201_Ok(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201, auth=False)

    def testPost400_WrongJSON(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400, expected_status_code=400, auth=False)


class AchievementDetailTestCase(LocalBaseTestCase):
    """
    Тесты для детального представления ачивок
    """
    def setUp(self):
        super().setUp()
        self.old_path = self.path
        self.path += f'{self.ach.id}/'
        self.path_404 = self.old_path + '100000/'
        self.data_202 = {
            'name': 'PATCH',
        }
        self.data_400 = {
            'name': None,
        }

    def testGet200_Ok(self):
        response = self.get_response_and_check_status(url=self.path, auth=False, token=self.user_token)
        self.fields_test(response, ['id', 'name', 'descr', 'pic_id', 'created_dt'])

    def testGet200_Deleted(self):
        achd = Achievement.objects.create(name='Name', descr='descr', deleted_flg=True)
        _ = self.get_response_and_check_status(url=self.old_path+f'{achd.id}/?with_deleted=True', auth=False)

    def testGet404_DeletedNoQueryparam(self):
        achd = Achievement.objects.create(name='Name', descr='descr', deleted_flg=True)
        _ = self.get_response_and_check_status(url=self.old_path+f'{achd.id}/', expected_status_code=404, auth=False)

    def testGet404_WrongId(self):
        _ = self.get_response_and_check_status(url=self.path_404, expected_status_code=404, auth=False)

    def testPatch202_Ok(self):
        response = self.patch_response_and_check_status(url=self.path, data=self.data_202, auth=False)
        self.assertEqual(response['id'], self.ach.id, msg='Wrong id')
        self.assertEqual(response['name'], self.data_202['name'], msg='Wrong name')

    def testPatch400_WrongJSON(self):
        _ = self.patch_response_and_check_status(url=self.path, data=self.data_400, expected_status_code=400,
                                                 auth=False)

    def testPatch404_WrongId(self):
        _ = self.patch_response_and_check_status(url=self.path_404, data=self.data_202, expected_status_code=404,
                                                 auth=False)

    def testDelete204_Ok(self):
        _ = self.delete_response_and_check_status(url=self.path, auth=False)

    def testDelete404_WrongId(self):
        _ = self.delete_response_and_check_status(url=self.path_404, expected_status_code=404, auth=False)
