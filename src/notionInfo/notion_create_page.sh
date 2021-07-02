https://www.notion.so/niceguy1575/93832554048043f6bd72a7363a3bbf17
secret_y26nBuHVqyRK9yemOKgJrXo5nRE6mqP5Q1pmtBGqhBU

-- page create은 가능하지만, 해당 내용을 직접 적어줘야할 필요가 있음.

-- 주간보고 Page를 그대로 copy하는 방법을 채택

curl 'https://api.notion.com/v1/pages' \
  -H 'Authorization: Bearer '"secret_y26nBuHVqyRK9yemOKgJrXo5nRE6mqP5Q1pmtBGqhBU"'' \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2021-05-13" \
  --data '{
	"parent": { "page_id": "93832554048043f6bd72a7363a3bbf17" },
	"properties": {
		"Name": {
			"title": [
				{
					"text": {
						"content": "Tuscan Kale"
					}
				}
			]
		},
		"Description": {
			"rich_text": [
				{
					"text": {
						"content": "A dark green leafy vegetable"
					}
				}
			]
		},
		"Food group": {
			"select": {
				"name": "Vegetable"
			}
		},
		"Price": { "number": 2.5 }
	},
	"children": [
		{
			"object": "block",
			"type": "heading_2",
			"heading_2": {
				"text": [{ "type": "text", "text": { "content": "Lacinato kale" } }]
			}
		},
		{
			"object": "block",
			"type": "paragraph",
			"paragraph": {
				"text": [
					{
						"type": "text",
						"text": {
							"content": "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.",
							"link": { "url": "https://en.wikipedia.org/wiki/Lacinato_kale" }
						}
					}
				]
			}
		}
	]
}'


-- 복사할 page get
-- page title만 확보 가능

curl 'https://api.notion.com/v1/pages/93832554048043f6bd72a7363a3bbf17' \
  -H 'Notion-Version: 2021-05-13' \
  -H 'Authorization: Bearer '"secret_y26nBuHVqyRK9yemOKgJrXo5nRE6mqP5Q1pmtBGqhBU"''



-- database get은? 불가능!

curl -X POST 'https://api.notion.com/v1/databases/93832554048043f6bd72a7363a3bbf17/query' \
  -H 'Authorization: Bearer '"secret_y26nBuHVqyRK9yemOKgJrXo5nRE6mqP5Q1pmtBGqhBU"'' \
  -H 'Notion-Version: 2021-05-13' \
  -H "Content-Type: application/json" \
	--data '{
	  "filter": {
	    "or": [
	      {
	        "property": "In stock",
					"checkbox": {
						"equals": true
					}
	      },
	      {
					"property": "Cost of next trip",
					"number": {
						"greater_than_or_equal_to": 2
					}
				}
			]
		},
	  "sorts": [
	    {
	      "property": "Last ordered",
	      "direction": "ascending"
	    }
	  ]
	}'

