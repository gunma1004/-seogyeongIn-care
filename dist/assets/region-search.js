document.addEventListener("DOMContentLoaded", function() {
    // 요소 가져오기
    var searchInput = document.getElementById("regionSearchInput");
    var searchResults = document.getElementById("regionSearchResults");
    
    // HTML 내부 스크립트로 정의된 데이터 가져오기 (메인1.txt 구조 반영)
    var searchData = window.__REGION_SEARCH__ || [];

    if (!searchInput || !searchResults) return;

    // 입력 이벤트 리스너
    searchInput.addEventListener("input", function(e) {
        var keyword = e.target.value.trim().toLowerCase();
        
        // 검색어가 없으면 창 숨기기
        if (!keyword) {
            searchResults.innerHTML = "";
            searchResults.style.display = "none";
            return;
        }

        // 키워드가 포함된 데이터 필터링
        var filtered = searchData.filter(function(item) {
            return item.keys && item.keys.toLowerCase().indexOf(keyword) !== -1;
        });

        // 결과 렌더링
        if (filtered.length > 0) {
            var html = filtered.map(function(item) {
                return '<a href="' + item.href + '"><strong>' + item.name + '</strong> <span style="color:#666; font-size:13px; margin-left:8px;">' + item.brand + '</span></a>';
            }).join("");
            searchResults.innerHTML = html;
            searchResults.style.display = "block";
        } else {
            searchResults.innerHTML = '<div class="noResult">검색 결과가 없습니다.</div>';
            searchResults.style.display = "block";
        }
    });

    // 검색창 외부 클릭 시 드롭다운 닫기
    document.addEventListener("click", function(e) {
        if (!e.target.closest('.searchControl')) {
            searchResults.style.display = "none";
        }
    });
});