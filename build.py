import json
import itertools
import os

os.makedirs('dist/homecare', exist_ok=True)

# 1. 업체 목록
partners = [
    {"name": "퀸즈홈테라피", "phone": "0507-1280-3296"},
    {"name": "한국미인테라피", "phone": "0507-1280-3140"},
    {"name": "오늘밤테라피", "phone": "0507-1280-3199"},
    {"name": "주주테라피", "phone": "0507-1280-3197"},
    {"name": "기쁨테라피", "phone": "0507-1280-3183"},
    {"name": "미인클럽테라피", "phone": "0507-1280-3180"}
]
partner_cycler = itertools.cycle(partners)

# 2. 서울 25개 자치구 및 주요 상권 (위도/경도/주소 완벽 매핑)
regions = [
    # 기존 데이터 기준 자치구 및 주요 지역
    {"region": "서울 강남", "slug": "seoul-gangnam", "city": "서울시 강남구", "lat": 37.4979, "lng": 127.0276, "addr": "테헤란로 152 인근"},
    {"region": "서울 송파", "slug": "seoul-songpa", "city": "서울시 송파구", "lat": 37.5145, "lng": 127.1059, "addr": "올림픽로 300 인근"},
    {"region": "서울 마포", "slug": "seoul-mapo", "city": "서울시 마포구", "lat": 37.5663, "lng": 126.9019, "addr": "월드컵북로 396 인근"},
    {"region": "서울 영등포", "slug": "seoul-yeongdeungpo", "city": "서울시 영등포구", "lat": 37.5258, "lng": 126.9241, "addr": "국제금융로 10 인근"},
    {"region": "서울 용산", "slug": "seoul-yongsan", "city": "서울시 용산구", "lat": 37.5299, "lng": 126.9648, "addr": "한강대로 405 인근"},
    {"region": "서울 성동", "slug": "seoul-seongdong", "city": "서울시 성동구", "lat": 37.5446, "lng": 127.0557, "addr": "아차산로 100 인근"},
    {"region": "서울 강서", "slug": "seoul-gangseo", "city": "서울시 강서구", "lat": 37.5602, "lng": 126.8335, "addr": "마곡중앙로 161 인근"},
    {"region": "서울 구로", "slug": "seoul-guro", "city": "서울시 구로구", "lat": 37.4955, "lng": 126.8877, "addr": "디지털로 300 인근"},
    {"region": "서울 노원", "slug": "seoul-nowon", "city": "서울시 노원구", "lat": 37.6543, "lng": 127.0568, "addr": "노해로 429 인근"},
    {"region": "서울 은평", "slug": "seoul-eunpyeong", "city": "서울시 은평구", "lat": 37.6176, "lng": 126.9227, "addr": "통일로 833 인근"},
    
    # 추가 15개 자치구 (센터 좌표 적용)
    {"region": "서울 강동", "slug": "seoul-gangdong", "city": "서울시 강동구", "lat": 37.5301, "lng": 127.1238, "addr": "성내로 25 인근"},
    {"region": "서울 강북", "slug": "seoul-gangbuk", "city": "서울시 강북구", "lat": 37.6392, "lng": 127.0255, "addr": "도봉로 89길 인근"},
    {"region": "서울 관악", "slug": "seoul-gwanak", "city": "서울시 관악구", "lat": 37.4782, "lng": 126.9515, "addr": "관악로 145 인근"},
    {"region": "서울 광진", "slug": "seoul-gwangjin", "city": "서울시 광진구", "lat": 37.5385, "lng": 127.0823, "addr": "자양로 116 인근"},
    {"region": "서울 금천", "slug": "seoul-geumcheon", "city": "서울시 금천구", "lat": 37.4519, "lng": 126.9020, "addr": "시흥대로 70 인근"},
    {"region": "서울 도봉", "slug": "seoul-dobong", "city": "서울시 도봉구", "lat": 37.6688, "lng": 127.0471, "addr": "마들로 656 인근"},
    {"region": "서울 동대문", "slug": "seoul-dongdaemun", "city": "서울시 동대문구", "lat": 37.5744, "lng": 127.0400, "addr": "천호대로 145 인근"},
    {"region": "서울 동작", "slug": "seoul-dongjak", "city": "서울시 동작구", "lat": 37.5120, "lng": 126.9397, "addr": "장승배기로 161 인근"},
    {"region": "서울 서대문", "slug": "seoul-seodaemun", "city": "서울시 서대문구", "lat": 37.5791, "lng": 126.9368, "addr": "연희로 248 인근"},
    {"region": "서울 서초", "slug": "seoul-seocho", "city": "서울시 서초구", "lat": 37.4837, "lng": 127.0324, "addr": "남부순환로 2584 인근"},
    {"region": "서울 성북", "slug": "seoul-seongbuk", "city": "서울시 성북구", "lat": 37.5894, "lng": 127.0167, "addr": "보문로 168 인근"},
    {"region": "서울 양천", "slug": "seoul-yangcheon", "city": "서울시 양천구", "lat": 37.5169, "lng": 126.8660, "addr": "목동동로 105 인근"},
    {"region": "서울 종로", "slug": "seoul-jongno", "city": "서울시 종로구", "lat": 37.5729, "lng": 126.9796, "addr": "종로1길 36 인근"},
    {"region": "서울 중구", "slug": "seoul-junggu", "city": "서울시 중구", "lat": 37.5636, "lng": 126.9975, "addr": "창경궁로 17 인근"},
    {"region": "서울 중랑", "slug": "seoul-jungnang", "city": "서울시 중랑구", "lat": 37.6065, "lng": 127.0927, "addr": "봉화산로 179 인근"},

    # 세부 동 단위 및 주요 상권 (기존 데이터 기준)
    {"region": "서울 신림", "slug": "seoul-sillim", "city": "서울시 관악구", "lat": 37.4842, "lng": 126.9297, "addr": "신림로 340 인근"},
    {"region": "서울 사당", "slug": "seoul-sadang", "city": "서울시 동작구", "lat": 37.4766, "lng": 126.9816, "addr": "동작대로 1 인근"},
    {"region": "서울 신촌", "slug": "seoul-sinchon", "city": "서울시 서대문구", "lat": 37.5553, "lng": 126.9368, "addr": "신촌로 83 인근"},
    {"region": "서울 홍대입구", "slug": "seoul-hongdae", "city": "서울시 마포구", "lat": 37.5572, "lng": 126.9245, "addr": "양화로 160 인근"},
    {"region": "서울 건대입구", "slug": "seoul-kondae", "city": "서울시 광진구", "lat": 37.5404, "lng": 127.0692, "addr": "능동로 110 인근"},
    {"region": "서울 왕십리", "slug": "seoul-wangsimni", "city": "서울시 성동구", "lat": 37.5615, "lng": 127.0378, "addr": "왕십리광장로 17 인근"},
    {"region": "서울 종로3가", "slug": "seoul-jongno3ga", "city": "서울시 종로구", "lat": 37.5704, "lng": 126.9912, "addr": "돈화문로 30 인근"},
    {"region": "서울 을지로", "slug": "seoul-euljiro", "city": "서울시 중구", "lat": 37.566, "lng": 126.991, "addr": "을지로 106 인근"},
    {"region": "서울 천호", "slug": "seoul-cheonho", "city": "서울시 강동구", "lat": 37.5386, "lng": 127.1238, "addr": "천호대로 1005 인근"},
    {"region": "서울 수유", "slug": "seoul-suyu", "city": "서울시 강북구", "lat": 37.638, "lng": 127.0256, "addr": "도봉로 338 인근"},
    {"region": "서울 미아사거리", "slug": "seoul-miasageori", "city": "서울시 강북구", "lat": 37.6133, "lng": 127.0301, "addr": "도봉로 45 인근"},
    {"region": "서울 신도림", "slug": "seoul-sindorim", "city": "서울시 구로구", "lat": 37.5088, "lng": 126.8913, "addr": "경인로 662 인근"},
    {"region": "서울 가산디지털", "slug": "seoul-gasan", "city": "서울시 금천구", "lat": 37.4811, "lng": 126.8827, "addr": "가산디지털1로 168 인근"},
    {"region": "서울 신정네거리", "slug": "seoul-sinjeong", "city": "서울시 양천구", "lat": 37.5202, "lng": 126.8529, "addr": "중앙로 261 인근"},
    {"region": "서울 공릉", "slug": "seoul-gongneung", "city": "서울시 노원구", "lat": 37.6256, "lng": 127.0731, "addr": "동일로 1078 인근"},
    {"region": "서울 구파발", "slug": "seoul-gupabal", "city": "서울시 은평구", "lat": 37.6368, "lng": 126.9188, "addr": "진관2로 15 인근"},
    {"region": "서울 중구 장충동", "slug": "jangchung", "city": "서울시 중구 장충동", "lat": 37.5621, "lng": 127.0044, "addr": "장충단로 59 인근"}
]

for region_data in regions:
    partner = next(partner_cycler)
    clean_phone = partner['phone'].replace('-', '')
    
    # JSON-LD 구조화 데이터 동적 생성
    json_ld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": partner['name'],
        "telephone": partner['phone'],
        "priceRange": "₩80,000~",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": region_data['city']
        },
        "description": f"{region_data['city']} 출장마사지 및 방문 바디케어 전문",
        "url": f"https://seogyeongIn-care.netlify.app/homecare/{region_data['slug']}.html"
    }

    # 서브 페이지 HTML 템플릿 
    html_content = f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{region_data['region']} {partner['name']} | 출장마사지 · 서경인케어맵</title>
  <meta name="description" content="{region_data['region']} 방문 바디케어 상세 정보">
  <link rel="canonical" href="https://seogyeongIn-care.netlify.app/homecare/{region_data['slug']}.html">
  <link rel="stylesheet" href="/assets/style.css">
  <script type="application/ld+json">
  {json.dumps(json_ld, ensure_ascii=False, indent=4)}
  </script>
</head>
<body>
  <!-- 상단 정보 영역 -->
  <section class="areaHero detail">
    <div class="wrap">
      <div class="detailTop">
        <div>
          <span class="tier vip">VIP</span>
          <h1>{partner['name']}</h1>
          <p>{region_data['city']} 생활권에서 방문 바디케어와 피로관리 정보를 찾는 분들을 위한 지역 파트너입니다. {region_data['region'].replace('서울 ', '')} 출장마사지를 비교할 때 필요한 정보를 확인하세요.</p>
        </div>
        <div class="priceBox">
          <span>기본요금</span><b>80,000원부터</b>
          <div class="priceActions">
            <a href="tel:{clean_phone}">전화</a>
            <a href="sms:{clean_phone}">문자</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 카카오 지도 영역 -->
  <section class="section compact storeMapSec" id="store-map">
    <div class="wrap">
      <div class="sectionHead">
        <div>
          <h2>{partner['name']} 매장 지도</h2>
          <p class="lead">{region_data['region']} 기준 위치를 카카오 지도에서 확인할 수 있습니다.</p>
        </div>
      </div>
      <div class="storeMapGrid">
        <div class="kakaoMapBox storeMapBox" id="storeMap_{region_data['slug']}">
          <div class="mapNeedKey">카카오 지도 로딩중입니다.</div>
        </div>
        <aside class="mapInfo storeMapInfo">
          <span class="tier vip">VIP</span>
          <h3>{partner['name']}</h3>
          <p>{region_data['region']} · {region_data['city']} {region_data['addr']}</p>
          <div class="mapInfoActions">
            <a class="btn primary" href="tel:{clean_phone}">전화</a>
            <a class="btn" href="sms:{clean_phone}">문자</a>
          </div>
        </aside>
      </div>
    </div>
    
    <!-- 카카오 맵 구동 스크립트 -->
    <script>
    (function(){{
      // ★ 여기에 카카오 JavaScript 키를 입력하세요.
      var key="d5bf2dca2a823214948b23ac0cdacbe5"; 
      var box=document.getElementById("storeMap_{region_data['slug']}");
      if(!box) return;
      
      function load(cb){{
        if(window.kakao&&window.kakao.maps){{kakao.maps.load(cb);return;}}
        var sc=document.createElement('script');
        sc.src='https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey='+encodeURIComponent(key)+'&v='+Date.now();
        sc.onload=function(){{kakao.maps.load(cb);}};
        document.head.appendChild(sc);
      }}
      
      load(function(){{
        box.innerHTML='';
        var pos=new kakao.maps.LatLng({region_data['lat']}, {region_data['lng']});
        var map=new kakao.maps.Map(box,{{center:pos,level:4}});
        map.addControl(new kakao.maps.ZoomControl(),kakao.maps.ControlPosition.RIGHT);
        
        var marker=new kakao.maps.Marker({{position:pos,map:map,title:"{partner['name']}",clickable:true}});
        var label=document.createElement('a');
        label.className='mapStoreLabel detailLabel vip';
        label.innerHTML='<b>{partner['name']}</b><span>상세페이지 이동</span>';
        
        new kakao.maps.CustomOverlay({{position:pos,content:label,yAnchor:1.75,zIndex:5}}).setMap(map);
      }});
    }})();
    </script>
  </section>
</body>
</html>"""
    
    file_path = f"dist/homecare/{region_data['slug']}.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        print(f"생성 완료 (지도 포함): {file_path}")
        import datetime

# --- 기존 지역별 HTML 생성 for문 종료 지점 (여기 아래부터 복사해서 붙여넣으세요) ---

# 3. robots.txt 자동 생성
robots_content = """User-agent: *
Allow: /

Sitemap: https://seogyeongIn-care.netlify.app/sitemap.xml
"""
with open('dist/robots.txt', 'w', encoding='utf-8') as f:
    f.write(robots_content)
    print("생성 완료: dist/robots.txt")

# 4. sitemap.xml 자동 생성
today = datetime.datetime.now().strftime('%Y-%m-%d')

# 사이트맵 헤더 및 메인 페이지 추가
sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://seogyeongIn-care.netlify.app/</loc>
        <lastmod>{today}</lastmod>
        <priority>1.0</priority>
    </url>"""

# 각 지역별 서브 페이지를 사이트맵에 반복 추가
for region_data in regions:
    url = f"https://seogyeongIn-care.netlify.app/homecare/{region_data['slug']}.html"
    sitemap_xml += f"""
    <url>
        <loc>{url}</loc>
        <lastmod>{today}</lastmod>
        <priority>0.8</priority>
    </url>"""

# 사이트맵 닫기
sitemap_xml += "\n</urlset>"

with open('dist/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap_xml)
    print("생성 완료: dist/sitemap.xml")