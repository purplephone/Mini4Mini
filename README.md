# Mini 4 Mini
## 소개
#### 항해 프로젝트를 위한 프로젝트
#### 항해 프로젝르를 진행하며 겪게 되는 trouble shooting 내용을 포스팅하고 공유해보세요!!
#### 이슈가 발생한 코드 or 에러 내용의 이미지 업로드가 가능합니다.
#### 좋아요를 통해 즐겨찾기에 추가 후 확인 가능

## 사이트 링크
http://limjae.shop/

## 화면
* 로그인 페이지
![loginpage](https://user-images.githubusercontent.com/43942574/157579714-8a67fa13-a52a-4d11-bef9-2bb341cb92a0.png)

* 회원가입 페이지
![signUpPage](https://user-images.githubusercontent.com/43942574/157579822-0e4ea9b6-0655-4e5c-927f-5c7797ddfa81.png)

* 메인 페이지
![메인페이지](https://user-images.githubusercontent.com/43942574/157593547-33b97e4c-1a5a-4f7f-be02-29f3b3bea136.png)

* 작성 및 수정 페이지
![삭제및수정페이지](https://user-images.githubusercontent.com/43942574/157593563-2453baf0-91ca-473d-976b-a75a99645159.png)


## 기능
* ID, password, 닉네임, 이메일, 전화번호 입력으로 간단한 회원가입 기능
* 목록 선택을 통해 확인하길 원하는 내용 확인 기능
* sorting을 통해 최신순, 추천순, 과거순 정렬 기능
* 글을 작성하고 사이트에 포스팅하는 기능 (card 형식)
* 이미지 업로드 및 업데이트 기능
* 목록에서 게시물 선택시 사용자에게 게시물 내용을 확인하는 기능(modal)
* 자신의 게시물 편집 및 삭제 기능


## 사용 기술
#### front-end
* jQuery
* bulma
* jinja2
* bootstrap
* html/css

#### back-end
* flask
* mongoDB

#### token
* JWT

## python package
* flask
* pymongo
* dnspython
* pyJWT
* jinja2
* certifi

## config.ini
```C
  SECRET_KEY = env['SECRET_KEY']['KEY']
  DB_LINK = env['DB_LINK']['LINK']
```
