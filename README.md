# jdspider
#### 用户自定义爬虫

- 功能描述：
用户只需要给定爬取字段的规则，就可以自动获取网页上所需要的字段信息。对于一些特殊网页，需要执行某些动作才能获取目标内容的，我们也提供了相应的自动执行动作的功能，用户可以根据自己的需求自由指定需要的动作类型（有些动作有靶向元素的还需要给出靶向元素的定位规则），然后填写该动作执行后的所需要获取的字段规则即可。如果有需要，也可以一次执行多次、多种动作，动作将按顺序依次执行，最终将返回所有动作所获取的汇总信息。信息可以选择保存至MongoDB。指定完具体的任务之后，用户就可以给出一个URL列表进行批量操作。
- 新增：
1. 增加了列表类型的页面爬取，此次增加是为了扩充功能，本功能为可选项
2. 功能说明：列表类型是指在一个网页中有许多相同类型的元素。以京东网页https://search.jd.com/Search?keyword=ipad&page=3为例，在一个页面中的这些商品列表中，每一个产品可看作重复出现的元素，那么我们就以一个产品作为基本元素，定义其规则后，就可以批量获取所有类似的元素。
3. 用户操作说明：此功能在增加功能的同时也对用户提出较高的要求，即用户必须对xpath规则有一定了解。我们假定用户了解xpath查询规则
4. 操作流程：1、用户需要给出一个卡片完整的父元素路径，比如上述网页中，应该需要找到能够代表一个卡片的xpath规则如："//div[@class="gl-i-wrap"]"，然后再找到该父元素的子元素作为字段提取的规则如title字段的"//div[@class="p-name p-name-type-2"]//em"，或者如price字段的"//div[@class=\"p-price\"]"，您也可以直接在浏览器开发者工具中将父元素和子元素的路径拼接成全路径进行验证。