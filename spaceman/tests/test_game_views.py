import json
from unittest.mock import *

from django.http.request import HttpRequest
from django.test import TestCase
from more_itertools.more import side_effect
from rest_framework.test import APIRequestFactory

from game_api.models import Game
from game_api.views import *


class GameApiViewTests( TestCase ):

    def setUp( self ):
        self.expected_game_data = {
            'guesses_allowed': 5,
            'guesses_taken': 3,
            'letters_guessed': ['A'],
            'guessed_word_state': ['', 'A'],
            'is_game_over': False,
            'id': None
        }

        self.mock_game = Game(
                word = "TESTWORD",
                guesses_allowed = self.expected_game_data['guesses_allowed'],
                guesses_taken = self.expected_game_data['guesses_taken'],
                letters_guessed = self.expected_game_data['letters_guessed'],
                guessed_word_state = self.expected_game_data['guessed_word_state'],
                is_game_over = self.expected_game_data['is_game_over']
            )

        self.request_factory = APIRequestFactory()
        self.mock_get_request = self.request_factory.get('dummy')


    ### POST (create game) view
    def test_game_view_should_create_new_game_on_POST( self ):
        response = game_view( self.request_factory.post('dummy') )

        self.assertEquals( response.status_code, 200)
        self.assertIsNotNone( response.data['id'] )
        self.assertTrue( response.data['id'] >= 0 )

    ### PUT (guess letter) view 
    def test_game_view_should_create_update_guesses_on_PUT( self ):
        with patch.object( Game.objects, 'get' ) as mock_get:
            self.mock_game.letters_available = ['B','C']
            mock_get.return_value = self.mock_game

            mock_request = self.request_factory.put( 'dummy', json.dumps({'letters_guessed': ['B']}), content_type='application/json')

            response = game_view( mock_request, 25 )
            
            mock_get.assert_called_with( pk=25 )
            self.assertEquals( response.status_code, 200 )
            self.assertEquals( response.data['letters_guessed'], ['A','B'])

    def test_game_view_should_reject_PUT_if_invalid( self ):
        with patch.object( Game.objects, 'get' ) as mock_get:
            self.mock_game.letters_available = ['B','C']
            mock_get.return_value = self.mock_game

            mock_request = self.request_factory.put( 'dummy', json.dumps({'letters_guessed': ['A']}), content_type='application/json')

            response = game_view( mock_request, 25 )
            
            mock_get.assert_called_with( pk=25 )
            self.assertEquals( response.status_code, 400 )


    ### GET solution view
    # TODO: Add tests for Getting a game's solution
    # HINT: remember the `setUp` fixture that is in this test class, 
    #   it constructs things that might be useful

    def test_get_solution_if_solution_is_found(self):
        with patch.object(Game.objects, 'get') as mock_get:
            self.mock_game.word = 'tony stark'
            mock_get.return_value = self.mock_game

            response = game_solution(self.mock_get_request, 25)

            mock_get.assert_called_with(pk = 25) 
            self.assertEqual (response.status_code, 200)

            test_solution = {'solution' : 'tony stark'}
            self.assertDictEqual(response.data, test_solution)


    def test_get_solution_show_404_if_game_id_is_not_found(self):
        with patch.object(Game.objects, 'get' ) as mock_get:
            mock_get.side_effect = Game.DoesNotExist 

            response = game_solution(self.mock_get_request, 25)
            self.assertEqual(response.status_code, 404)

            
