import requests
import json
import os


class TestApi:

    # frequency tests

    def test_frequency_not_ajax(self):
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/frequency/")
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_frequency_not_post(self):
        response = requests.get(f"http://{os.environ.get('BASE_URL')}:8000/seo/frequency/", headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_frequency_no_data(self):
        payload = json.dumps("")
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/frequency/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_frequency_correct_frequency(self):
        payload = json.dumps("django est django")
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/frequency/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json'})
        assert response.content == b'[["django", 2]]'

    # check_keyword tests

    def test_check_keyword_not_ajax(self):
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/keyword/")
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_keyword_not_post(self):
        response = requests.get(f"http://{os.environ.get('BASE_URL')}:8000/seo/keyword/", headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_keyword_no_data(self):
        payload = json.dumps([])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/keyword/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_keyword_no_keyword(self):
        payload = json.dumps(["", ""])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/keyword/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json'})
        assert response.content == b'{"response": "NO_KEYWORD"}'

    def test_check_keyword_no_text(self):
        payload = json.dumps(["django", ""])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/keyword/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json'})
        assert response.content == b'{"response": "NO_TEXT"}'

    def test_check_keyword_valid(self):
        payload = json.dumps(
            ["django", "django est un framework basé sur la technologie python pour faciliter la création de sites web solides et sécurisé tout en apportant les avantages d’une architecture pensée de manière optimisée et facile d’utilisation. C’est un framework intéressant."])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/keyword/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json'})
        assert response.content == b'{"response": "VALID_KEYWORD", "percentage": 2.7027027027027026}'

    def test_check_keyword_invalid(self):
        payload = json.dumps(
            ["django", "django"])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/keyword/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json'})
        assert response.content == b'{"response": "INVALID_KEYWORD", "percentage": 100.0}'

    # article_length tests

    def test_article_length_not_ajax(self):
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/length/")
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_article_length_not_post(self):
        response = requests.get(f"http://{os.environ.get('BASE_URL')}:8000/seo/length/", headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_article_length_no_data(self):
        payload = json.dumps("")
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/length/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_article_length_bad(self):
        payload = json.dumps("django")
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/length/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"code": 0, "length": 1}'

    def test_article_length_average(self):
        payload = json.dumps("Django Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam non nisl neque. Sed et efficitur nunc. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras dui sem, efficitur vitae pharetra vel, auctor nec lorem. Proin scelerisque dui in est blandit fringilla. Pellentesque iaculis efficitur purus, sed tincidunt leo maximus eu. In ultrices massa viverra magna pellentesque dapibus. Vestibulum non eros tincidunt, tempus turpis ut, maximus velit. Nulla porta leo lobortis odio tincidunt ornare. Quisque lobortis auctor ante, sit amet fermentum quam egestas ac. Cras ut aliquet risus. Proin ac massa in elit eleifend porttitor sed non ante.Duis facilisis nisi in elit vehicula tincidunt. Nunc varius augue nec interdum semper. Ut elit tortor, bibendum vel iaculis in , consequat nec purus. Aliquam pellentesque id tortor congue facilisis. Nam hendrerit feugiat est vel consequat. Aliquam bibendum maximus libero. Nam ullamcorper consequat lobortis. Proin mi odio, ullamcorper in placerat nec, ornare quis tortor. Nullam sit amet tortor sit amet quam tincidunt semper in vulputate augue. Praesent et ultrices velit.Vestibulum et egestas urna. Aliquam erat volutpat. Pellentesque in risus ut tellus rhoncus mattis id eget lectus. Vivamus in faucibus ipsum, et auctor justo. Proin vestibulum eu felis non bibendum. Maecenas varius neque mauris, a venenatis felis efficitur in . Aenean sed ultrices nunc. Quisque posuere augue diam, nec congue ex pretium at. Vivamus ut consequat magna. Sed lacinia, est vehicula pulvinar viverra, erat metus euismod nunc, non mattis turpis odio et libero. Aenean faucibus, elit et ullamcorper elementum, justo ligula tincidunt massa, eu sollicitudin arcu libero in risus. Quisque vehicula turpis eu augue sagittis, ut commodo est ornare. Phasellus ultrices, justo vitae imperdiet vulputate, dui augue condimentum tellus, quis facilisis ligula nunc eu velit. In hac habitasse platea dictumst.Quisque diam nibh, blandit ut nisl a, consequat pharetra sapien. Pellentesque nec fermentum arcu. Morbi vel dolor varius, sollicitudin erat sit amet, fermentum tortor. Nulla mauris lacus, feugiat vel nisl ac, fermentum consequat velit. Praesent pretium odio nec enim euismod mattis. Aenean non urna a mi porta placerat. Quisque sit amet rutrum enim. Aliquam dictum arcu sed vulputate tincidunt. Duis id ultrices lectus.Curabitur orci lectus, cursus vel imperdiet congue, imperdiet id eros. Nullam pulvinar, neque sed volutpat tempus, risus odio elementum nulla, at laoreet lectus urna quis erat. Donec eu blandit nunc, vel ultricies felis. Maecenas eget ex ut quam eleifend accumsan at vitae enim. Nam aliquam non augue id porttitor. Curabitur mauris turpis, tincidunt a tincidunt eu, suscipit sit amet justo. Mauris lacus libero, laoreet nec interdum porta, rhoncus et mi. Sed suscipit interdum suscipit. Nunc eleifend nisl enim, ut pulvinar turpis efficitur et. Maecenas at pretium dolor, eget pulvinar purus. Nunc accumsan, magna maximus ultricies congue, leo nisi ultrices ipsum, nec sodales leo purus porttitor nunc.Phasellus eget viverra metus. Cras sed purus vel diam sollicitudin scelerisque et sed sapien. Ut dictum sollicitudin bibendum. Quisque sit amet quam ut lacus viverra laoreet et ut tortor. Sed dictum eros ac nulla pellentesque condimentum. Quisque auctor aliquam lorem, ac maximus est interdum a. Phasellus ante metus, dapibus non massa in , convallis ultricies eros. Aenean quam metus, scelerisque id tellus vel, hendrerit blandit odio. Etiam feugiat mollis magna, eget vulputate lorem ultrices eget. Vestibulum a condimentum quam, sit amet pharetra massa. Fusce vel tellus nisi. Nullam eget magna semper eros eleifend aliquam sit amet eu ex. Maecenas sed faucibus nulla.Nullam ullamcorper elit felis, eget pharetra sem porttitor quis. Nulla dictum malesuada neque, sit amet aliquet nunc molestie et. Etiam lobortis neque sit amet venenatis tempus. Nullam ultricies lorem velit, et tincidunt tellus fermentum eu. Quisque tincidunt sem at mi semper consequat. Cras id fermentum diam. Proin pharetra velit a massa condimentum sodales. Cras sollicitudin ultrices sapien, quis suscipit magna gravida ac. In hac habitasse platea dictumst. Duis id viverra lectus, et pulvinar ex.Curabitur laoreet, sapien non tempor elementum, dolor nisi consectetur neque, at lacinia erat magna in nisi. Mauris consectetur, purus at pulvinar mollis, nunc mauris tempus justo, at efficitur nulla nulla at neque. Aenean consequat, massa ut volutpat dignissim, tortor nisl pulvinar ipsum, id finibus orci arcu sit amet mauris. Maecenas sed nisl ac purus consequat egestas non aliquam magna. Integer ut neque porta, cursus erat a, ornare arcu. Integer erat enim, auctor pretium varius vitae, auctor id dui. Quisque hendrerit vulputate augue, sed rhoncus dolor malesuada varius. Donec molestie leo nec velit mattis tincidunt. Integer commodo quam eu condimentum placerat. Pellentesque eleifend vel mi quis commodo. Quisque ultrices, dolor a auctor sollicitudin, ipsum ipsum maximus est, vel pellentesque magna velit congue lacus. Proin ornare hendrerit odio. Donec blandit in ipsum id sodales. Integer at sapien eu nulla posuere finibus gravida vel tellus.Aenean eu dictum lectus. Mauris varius scelerisque aliquet. Duis lacinia, nibh quis finibus congue, lacus dui lobortis erat, rutrum scelerisque sem quam sed arcu. Nulla dignissim placerat ante eget tristique. Curabitur id sollicitudin magna, vitae pretium nibh. Cras libero lorem, pulvinar at condimentum sed, rhoncus vel lectus. Quisque accumsan sed nibh a lacinia. Nunc posuere elementum ante, et dignissim erat rutrum a. Ut ligula neque, dapibus eu venenatis ut, sodales ac justo. Mauris commodo, nibh ut blandit mollis, justo purus luctus justo, eu consectetur neque nisi et mauris.Maecenas accumsan orci ante. Proin faucibus at orci vitae tincidunt. Nulla vel risus aliquam, sagittis urna et, ultricies libero. Phasellus eleifend eleifend nulla eu bibendum. Pellentesque sed egestas tortor. Mauris leo massa, aliquet ac est in , tristique scelerisque ex. Suspendisse mattis iaculis. Pellentesque sed egestas tortor. Mauris leo massa, aliquet ac est in , tristique scelerisque ex. Suspendisse mattis iaculis.")
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/length/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"code": 1, "length": 910}'

    def test_article_length_good(self):
        payload = json.dumps("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus consequat, mauris in tincidunt dapibus, magna metus rhoncus risus, vitae rutrum leo ante a justo. Ut consequat mauris eget quam tempor fermentum. Praesent vel mauris lorem. Nunc eget lorem placerat, fermentum sapien vel, scelerisque libero. Suspendisse potenti. Pellentesque vel pulvinar justo. Nullam vitae vulputate urna. Integer cursus diam semper neque laoreet vestibulum. Aliquam lorem odio, tristique quis ligula sed, suscipit dictum lectus. Nulla a neque porttitor, volutpat ipsum in , fringilla velit. Vestibulum ultricies, augue quis interdum porttitor, tortor ante tincidunt dui, hendrerit congue sem leo non metus. Nullam in accumsan nulla. Phasellus vulputate eleifend dolor eget lobortis. Integer viverra mattis est id vestibulum. Etiam tempus metus sed rhoncus tempus.Proin mauris enim, vestibulum in varius et, malesuada eget neque. Etiam fermentum mi ut tristique rutrum. Sed porttitor neque nec ligula finibus ullamcorper. Aenean at massa non nisi convallis finibus. Duis est tortor, blandit eu lobortis id, accumsan eget sapien. Aliquam eu gravida tellus, vitae faucibus velit. Aenean placerat, odio et rutrum tempor, massa turpis finibus libero, in malesuada tortor nibh eu lectus. Proin in libero in leo vestibulum pharetra. Sed semper ipsum ac laoreet commodo. Duis ut viverra nisi, a faucibus erat. Sed sed egestas enim. Praesent nec venenatis lacus. Ut vel lacinia risus. Fusce eget dui porta, lacinia lacus tempor, finibus nisl. Vivamus imperdiet felis eu ullamcorper mollis. Nulla eget enim feugiat, pulvinar ex a, fermentum dolor.Nullam commodo porttitor nunc, blandit varius dolor placerat ut. Mauris a massa fermentum, finibus lorem nec, auctor lectus. Donec nisi sapien, finibus ac sem eu, consectetur semper mauris. Morbi finibus magna eros. Phasellus scelerisque sit amet lorem sit amet mattis. Nulla elementum vitae ipsum id porttitor. Proin tincidunt sem in quam rhoncus, in elementum lorem vehicula. Integer a euismod ligula, ac malesuada turpis. Fusce odio tortor, dignissim non pharetra et, varius ac lectus. Pellentesque sit amet dolor non arcu interdum vestibulum at id lorem. Duis egestas semper velit, vitae laoreet mauris pulvinar nec. Mauris tortor nunc, pulvinar a tellus ac, porttitor vehicula augue. Maecenas quis sollicitudin nibh, ac porta turpis. Phasellus maximus quam vel enim malesuada, varius tempus leo luctus.Aliquam erat volutpat. Nam finibus rutrum facilisis. Integer tincidunt felis facilisis, consectetur augue a, euismod justo. Etiam feugiat porttitor rhoncus. Proin odio tortor, finibus et pharetra a, bibendum et dolor. Suspendisse imperdiet sodales velit sed luctus. Duis et diam id dui accumsan eleifend at vitae eros. Donec id eros non purus luctus maximus. Proin vehicula viverra nisl, accumsan placerat nisi sodales at. Suspendisse faucibus velit id erat sagittis, sit amet fringilla neque cursus.Pellentesque sit amet dui luctus, interdum velit dignissim, sollicitudin dui. Cras eu turpis at orci finibus sollicitudin a eget tellus. Nunc iaculis finibus vestibulum. In eget ultrices dolor. Vivamus eget arcu vitae nulla sodales molestie tincidunt ut sapien. Sed euismod tortor tellus, eu dictum metus fringilla at. Sed ac enim interdum, lobortis enim a, lobortis eros. Proin iaculis tortor dui. Morbi elementum purus maximus laoreet pulvinar. Donec ut diam non tellus vestibulum lobortis. Fusce non tempor purus. Ut fringilla massa in enim vehicula, sed euismod augue tristique. Donec quam ex, mollis non massa sit amet, interdum ultrices velit. Integer eget lectus nec ligula euismod commodo eu id magna. Nulla facilisi.Nam volutpat rutrum ante in finibus. Nulla cursus tellus est, id lobortis justo euismod eget. Praesent aliquam maximus nunc. Cras quis dignissim massa. Suspendisse imperdiet erat et consectetur luctus. Nam vel tortor sed nunc imperdiet finibus. Phasellus fermentum ligula sed dolor lobortis semper. Nulla tincidunt lectus vel ullamcorper venenatis. Sed quis dui rutrum, rhoncus diam et, sagittis mi. Nam ut enim ante. Integer scelerisque metus in lacus porttitor, non fermentum lacus venenatis.Praesent porta semper turpis, malesuada pharetra urna posuere ac. Vivamus nec pharetra massa. Aliquam fermentum, metus et gravida cursus, erat nibh aliquet nulla, ac posuere metus leo elementum elit. Phasellus a justo ac magna auctor ultricies. Nam aliquet at massa ut suscipit. Nulla ornare eget libero vel facilisis. Donec nec rhoncus nibh. Aenean est nisi, posuere at nisi vel, commodo iaculis orci. Suspendisse ipsum enim, convallis varius risus sed, accumsan ullamcorper elit. Aenean non lectus ornare, malesuada purus quis, fermentum enim. Sed consectetur dolor metus, id auctor justo ultricies sit amet.Proin sodales aliquet libero id ultricies. Fusce vitae condimentum neque. Nam eget libero non nisi porttitor euismod et at augue. Nulla vulputate id lectus elementum condimentum. Aliquam a nisi eu odio pretium fringilla in id orci. Nunc libero neque, viverra nec venenatis at, consequat vel lacus. Nullam vel justo nibh.Maecenas non diam quis ligula commodo semper. Fusce lobortis augue vitae mi sodales, a ultrices sapien vehicula. Proin blandit, ligula at varius placerat, mauris enim blandit enim, eget congue lacus urna non odio. Nam facilisis lorem vitae sem euismod, sodales viverra ex hendrerit. Proin gravida congue mi. Aenean condimentum magna tincidunt dui cursus mollis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed luctus urna et sem dictum, sed vehicula turpis placerat. Donec semper elit ut ligula ullamcorper, quis mattis lorem molestie. Vivamus quis commodo sapien, semper maximus nisl. Morbi nec enim a odio placerat mattis.Cras eget diam porttitor, ullamcorper neque pharetra, molestie ante. Nulla vitae nulla sodales, aliquam felis sed, feugiat magna. Pellentesque ac egestas ante. Aenean a ante accumsan, porttitor risus eget, mollis lectus. Aenean pretium volutpat urna, dignissim ultrices nisi euismod cursus. Donec ullamcorper justo ante, ac rutrum magna tristique sit amet. Pellentesque tortor libero, sollicitudin a pellentesque ac, rhoncus eget felis.Suspendisse potenti. Quisque neque elit, ultricies at ullamcorper ac, malesuada ac ligula. Ut rutrum malesuada ornare. Phasellus pretium, nibh eget molestie sagittis, risus libero consequat orci, eget venenatis quam erat nec neque. Phasellus maximus ornare tempor. Vivamus felis nunc, molestie sit amet blandit eget, consequat eu dolor. In est nisi, suscipit fringilla ante in , finibus commodo justo. Fusce dictum lacus vitae tincidunt elementum. Morbi ut velit quis est lacinia vestibulum id in purus. Donec pulvinar metus turpis. Aliquam cursus nisi ac posuere consectetur. Nulla eu blandit turpis.Aenean id massa eu metus dignissim vulputate. Pellentesque vehicula turpis aliquam mi aliquet ullamcorper. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Aenean lacinia egestas neque vitae bibendum. Nulla iaculis purus ac ante ultricies, finibus faucibus urna aliquam. Praesent vitae dictum ex, quis ultricies odio. Proin in laoreet lacus. Aenean pellentesque dapibus purus, cursus eleifend ante varius non.Sed feugiat eros risus, eget efficitur orci pulvinar in . Ut nec quam a nunc maximus porta a nec arcu. Mauris non dui augue. Integer porttitor ligula et turpis consectetur, at fringilla elit posuere. Fusce vel rhoncus ipsum. Duis mi turpis, mollis vel erat a, pellentesque tempus lectus. Phasellus faucibus hendrerit cursus. Integer consectetur tempus massa. Pellentesque in facilisis magna, eu sagittis est. Etiam sodales dui at augue bibendum placerat. Nulla facilisi. Curabitur consectetur euismod sapien, nec eleifend nisi venenatis ac. Phasellus sit amet orci lectus. Vivamus orci urna, ultrices in sapien ac, hendrerit sodales metus.Duis ante urna, vulputate nec justo gravida, posuere convallis felis. Aenean id sapien sit amet tellus tincidunt porta quis vel lorem. Quisque sollicitudin ultrices nisi. Vestibulum ornare quam ut viverra laoreet. Donec lobortis sapien ut nulla sollicitudin, maximus pellentesque velit pellentesque. Ut interdum risus velit, id dignissim dolor pretium ac. Nunc interdum venenatis justo quis suscipit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Aliquam lobortis tellus eget odio ornare, sit amet blandit eros condimentum.Donec nec odio iaculis, hendrerit nibh quis, imperdiet mi. Vivamus elementum porttitor semper. Quisque sagittis varius neque, vitae porttitor risus sagittis a. Donec vitae nisi sit amet elit ornare mollis ut eget urna. Proin elementum orci leo, sit amet mollis ligula vestibulum sit amet. Maecenas nulla nunc, interdum sit amet est ut, molestie sollicitudin diam. Curabitur efficitur sodales dictum. Sed dignissim lorem ut sem maximus suscipit.Aliquam nec felis eu nisi dapibus fringilla. Curabitur dolor sem, commodo ut tempor sed, condimentum nec odio. Aliquam at gravida odio. Vivamus egestas sodales lectus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Pellentesque pharetra ligula a dignissim semper. Nulla ac lacinia metus. Proin lobortis maximus ipsum et vehicula. Nam a eros posuere, rutrum enim eget, blandit diam.Nunc blandit ultrices erat, sed euismod diam mattis non. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curaIn porttitor augue sit amet volutpat tempus. Pellentesque finibus, augue non mattis eleifend, lacus leo varius justo, vitae ullamcorper nibh lectus eu justo. Sed imperdiet mi a accumsan congue. Pellentesque varius egestas tortor, ac tincidunt elit pharetra et. Quisque pretium non nibh ut dictum. Nunc eu convallis erat. Pellentesque iaculis id dui in tincidunt.Nulla tempor aliquam elit, non pellentesque lectus. Mauris tellus odio, mattis in velit sed, consectetur pulvinar urna. Curabitur tincidunt congue porttitor. Cras vehicula libero turpis, vel finibus turpis sodales et. Cras dignissim aliquet tortor, et dapibus arcu. Aliquam sed arcu eget magna imperdiet suscipit. Aenean consectetur neque risus, in ornare ligula pretium eget. In risus enim, feugiat ut sapien aliquet, scelerisque.")
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/length/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"code": 2, "length": 1482}'

    # check_title tests

    def test_check_title_not_ajax(self):
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title/")
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_title_not_post(self):
        response = requests.get(f"http://{os.environ.get('BASE_URL')}:8000/seo/title/", headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_title_no_data(self):
        payload = json.dumps([])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_title_no_keyword(self):
        payload = json.dumps(["", "django update"])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json'})
        assert response.content == b'{"response": "NO_KEYWORD", "character_count": 12, "word_count": 2}'

    def test_check_title_no_title(self):
        payload = json.dumps(["django", ""])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json'})
        assert response.content == b'{"response": "NO_TITLE"}'

    def test_check_title_valid(self):
        payload = json.dumps(["django", "django update is out right now check out"])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title/",
                                 data=payload,
                                 headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"response": "VALID_TITLE", "keyword_present": true, "character_count": 33, "word_count": 8}'

    def test_check_title_keywords_not_present(self):
        payload = json.dumps(["django python wagtail", "python is used by many developpers around the world"])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title/",
                                 data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"response": "INVALID_TITLE", "keyword_present": false, "character_count": 43, "word_count": 9}'

    def test_check_title_not_enough_words(self):
        payload = json.dumps(["django", "django is used by many"])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title/",
                                 data=payload,
                                 headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"response": "INVALID_TITLE", "keyword_present": true, "character_count": 18, "word_count": 5}'

    def test_check_title_too_many_words(self):
        payload = json.dumps(["django", "django is used by many and it is fast and check out this and this and this"])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title/",
                                 data=payload,
                                 headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"response": "INVALID_TITLE", "keyword_present": true, "character_count": 58, "word_count": 17}'

    def test_check_title_too_many_characters(self):
        payload = json.dumps(["django", "django is exceptionally orchestrated and exponentially, unassumingly overloaded"])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title/",
                                 data=payload,
                                 headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"response": "INVALID_TITLE", "keyword_present": true, "character_count": 71, "word_count": 8}'

    # check_slug tests

    def test_check_slug_not_ajax(self):
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/slug/")
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_slug_not_post(self):
        response = requests.get(f"http://{os.environ.get('BASE_URL')}:8000/seo/slug/", headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_slug_no_data(self):
        payload = json.dumps([])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/slug/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_slug_no_keyword(self):
        payload = json.dumps(["", ""])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/slug/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json'})
        assert response.content == b'{"response": "NO_KEYWORD"}'

    def test_check_slug_no_title(self):
        payload = json.dumps(["django", ""])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/slug/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json'})
        assert response.content == b'{"response": "NO_SLUG"}'

    def test_check_slug_valid(self):
        payload = json.dumps(["django python", "python-guide-django-update"])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/slug/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"response": "VALID_SLUG"}'

    def test_check_slug_invalid(self):
        payload = json.dumps(["django", "python"])
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/slug/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"response": "INVALID_SLUG"}'

    # check_internal_links tests

    def test_check_internal_links_not_ajax(self):
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/internal_links/")
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_internal_links_not_post(self):
        response = requests.get(f"http://{os.environ.get('BASE_URL')}:8000/seo/internal_links/", headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_internal_links_no_data(self):
        payload = json.dumps("")
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/internal_links/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_internal_links_bad(self):
        payload = json.dumps('<a href="http://www.google.com" role="button" class="TooltipEntity"></a><span data-offset-key="61sd6 - 0 - 0"><span data-text="true">eeiua </span></span>')
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/internal_links/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"code": 0, "internal_links": 0}'

    def test_check_internal_links_average(self):
        payload = json.dumps(
            f"""<a href="http://{os.environ.get('BASE_URL')}" role="button" class="TooltipEntity"></a><a href="https://{os.environ.get('BASE_URL')}" role="button" class="TooltipEntity"></a><a href="http://www.google.com" role="button" class="TooltipEntity"></a><a href="../../../../../../django" role="button" class="TooltipEntity"></a><a href="http://www.angular.io" role="button" class="TooltipEntity"></a><a href="http://www.facebook.com" role="button" class="TooltipEntity"></a>""")
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/internal_links/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"code": 1, "internal_links": 3}'

    def test_check_internal_links_good(self):
        payload = json.dumps(
            f"""<a href="./django" role="button" class="TooltipEntity"></a><a href="../django/" role="button" class="TooltipEntity"></a><a href="//{os.environ.get('BASE_URL')}" role="button" class="TooltipEntity"></a><a href="http://www.google.com" role="button" class="TooltipEntity"></a><a href="https://{os.environ.get('BASE_URL')}" role="button" class="TooltipEntity"></a><a href="/django/" role="button" class="TooltipEntity"></a>""")
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/internal_links/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"code": 2, "internal_links": 5}'

    # check_title_in_article tests

    def test_check_title_in_article_not_ajax(self):
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title_in_article/")
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_title_in_article_not_post(self):
        response = requests.get(f"http://{os.environ.get('BASE_URL')}:8000/seo/title_in_article/", headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_title_in_article_no_data(self):
        payload = json.dumps("")
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title_in_article/", data=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"error": "Request wrong formatted"}'

    def test_check_title_in_article_valid(self):
        payload = json.dumps('<span data-offset-key="61sd6 - 0 - 0"><span data-text="true">eeiua  '
                             + '</span></span><div>bonjour</div><h2>')
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title_in_article/",
                                 data=payload,
                                 headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"response": "NO_H1_PRESENT"}'

    def test_check_title_in_article_invalid(self):
        payload = json.dumps('<span data-offset-key="61sd6 - 0 - 0"><span data-text="true">eeiua '
                             + '</span></span><h2>secondary title</h2><h1>primary title</h1>')
        response = requests.post(f"http://{os.environ.get('BASE_URL')}:8000/seo/title_in_article/",
                                 data=payload,
                                 headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.content == b'{"response": "H1_PRESENT"}'
