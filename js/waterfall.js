/* jshint asi:true */
//先等图片都加载完成
//再执行布局函数

/**
 * 执行主函数
 * @param  {[type]} function( [description]
 * @return {[type]}           [description]
 */
(function() {

  /**
     * 内容JSON
     */
  var demoContent = [
    {
      demo_link: 'https://movie.douban.com/subject/26387939/',
      img_link: 'https://i.loli.net/2017/10/24/59eefa2bd0016.png',
      title: '摔跤吧！爸爸',
      key_word: '剧情 / 传记 / 运动',
      score: 9.1,
      description: '马哈维亚（阿米尔·汗 Aamir Khan 饰）曾经是一名前途无量的摔跤运动员，在放弃了职业生涯后，他最大的遗憾就是没有能够替国家赢得金牌。\n马哈维亚将这份希望寄托在了尚未出生的儿子身上，哪知道妻子接连给他生了两个女儿。让马哈维亚没有想到的是，两个姑娘展现出了杰出的摔跤天赋，让他幡然醒悟，就算是女孩，也能够昂首挺胸的站在比赛场上，为了国家和她们自己赢得荣誉......'
    }, 
    {
      demo_link: 'https://movie.douban.com/subject/26580232/',
      img_link: 'https://i.loli.net/2017/10/24/59eefa2b5383b.png',
      title: '看不见的客人',
      key_word: '悬疑 / 惊悚 / 犯罪',
      score: 8.7,
      description: '艾德里安（马里奥·卡萨斯 Mario Casas 饰）经营着一间科技公司，事业蒸蒸日上，家中有美丽贤惠的妻子和活泼可爱的女儿，事业家庭双丰收的他是旁人羡慕的对象。然而，野心勃勃的艾德里安并未珍惜眼前来之不易的生活，一直以来，他和一位名叫劳拉（芭芭拉·蓝妮 Bárbara Lennie 饰）的女摄影师保持着肉体关系......'
    }, 
    {
      demo_link: 'https://movie.douban.com/subject/26363254/',
      img_link: 'https://i.loli.net/2017/10/24/59eefa2bc4df7.png',
      title: '战狼2',
      key_word: '动作',
      score: 7.4,
      description: '故事发生在非洲附近的大海上，主人公冷锋（吴京 饰）遭遇人生滑铁卢，被“开除军籍”，本想漂泊一生的他，正当他打算这么做的时候，一场突如其来的意外打破了他的计划，突然被卷入了一场非洲国家叛乱，本可以安全撤离，却因无法忘记曾经为军人的使命，孤身犯险冲回沦陷区，带领身陷屠杀中的同胞和难民，展开生死逃亡。随着斗争的持续，体内的狼性逐渐复苏，最终孤身闯入战乱区域，为同胞而战斗......'
    }, 
    {
      demo_link: 'https://movie.douban.com/subject/26759539/',
      img_link: 'https://i.loli.net/2017/10/24/59eefa2bcafa8.png',
      title: '十万个冷笑话2',
      key_word: '喜剧 / 动画 / 奇幻',
      score: 7.5,
      description: '拥有着强大力量的创世神杖被四大神之一的埃及神拉（李璐 配音）盗走。为了令宇宙免于被毁灭的悲惨命运，希腊神宙斯（藤新 配音）派出了自己的女儿雅典娜（山新 配音）追踪神杖的下落。\n小金刚（皇贞季 配音）是自幼生长在孤儿院里的平凡少年，常年凭借着机灵的脑瓜靠着坑蒙拐骗赚钱度日，只为了有朝一日身患重病的青梅竹马小青（C小调 配音）能够康复。一次偶然中，小金刚得到了藏有创世神杖下落的藏宝图，随后遭到了雷神托尔（李姝洁 饰）的伏击，在争抢之中，藏宝图被破坏，就这样，小金刚成为了唯一一个知道创世神杖在哪里的凡人。就这样，小金刚、雅典娜、托尔，再加上一个来自东方的脱线河神（郝祥海 饰），一行四人踏上了寻找创世神杖的旅途......'
    }, 
    {
      demo_link: 'https://movie.douban.com/subject/27024903/',
      img_link: 'https://i.loli.net/2017/10/24/59eefa2b687a5.png',
      title: '天才枪手',
      key_word: '剧情 / 悬疑 / 犯罪',
      score: 8.3,
      description: '影片根据2014年轰动一时的亚洲考场作弊案改编，讲述了天才学霸利用高智商考场作弊牟取暴利的故事。出生平凡的天才少女Lynn（茱蒂蒙·琼查容苏因 饰）在进入贵族学校后，结识了富二代同学Grace（依莎亚·贺苏汪饰）与Pat（披纳若·苏潘平佑饰），从此开始了考场作弊生涯，与此同时，另一名记忆力极佳的天才学霸Bank（查侬·散顶腾古 饰）发现了Lynn不为人知的“交易”。经过多场险象环生的“作弊战争”后，Lynn接下最后一单在国际考场上为富家子弟作弊的天价委托。一场横跨两大洲的完美作弊方案横空出世，然而一切并不像他们想的那么简单......'
    },
    {
      demo_link: 'https://movie.douban.com/subject/10512661/',
      img_link: 'https://i.loli.net/2017/10/24/59eefa2bd002c.png',
      title: '银翼杀手',
      key_word: '科幻 / 惊悚',
      score: 8.4,
      description: '本片发生在前作30年后，新的银翼杀手、瑞恩·高斯林饰演的洛杉矶警察K发现一个足以颠覆社会的惊天秘密，这个发现让他开始寻找已经消失匿迹30年的前银翼杀手瑞克·戴克（哈里森·福特饰）......'
    },
    {
      demo_link: 'https://movie.douban.com/subject/25933890/',
      img_link: 'https://i.loli.net/2017/10/27/59f30de0e32ed.png',
      title: '极盗车神',
      key_word: '动作 / 音乐 / 犯罪',
      score: 7.1,
      description: 'Baby（安塞尔·艾尔高特 Ansel Elgort 饰）专门负责帮银行抢劫犯开车逃脱。Baby因童年的一场事故导致耳疾，要靠专属的音乐来掌控开车节奏。偶然的一次邂逅，他与餐厅女服务生（莉莉·詹姆斯 Lily James 饰）坠入爱河，并想就此金盆洗手。头目老大道哥（凯文·史派西 Kevin Spacey 饰）表示，只要Baby再完成最后一次任务，就可以给他自由。殊不知，巨大的危险和挑战在等待着Baby......'
    },
    {
      demo_link: 'https://movie.douban.com/subject/26908002/',
      img_link: 'http://i2.bvimg.com/617101/39e00e752576fa1at.jpg',
      title: '天赋异禀 The Gifted (2017)',
      key_word: '动作 / 科幻 / 奇幻',
      score: 8.2,
      description: 'Fox将推出全新X战警剧集，马特·尼克斯(《火线警告》)负责开发本剧。该剧讲述一对夫妇发现他们的孩子具有超能力，平静生活瞬间瓦解。而他们也不得不铤而走险，躲避当局，尼克斯表示本剧和大表哥的《军团》不同，该剧和“X战警”电影宇宙有密切联系，至于剧集角色，电影中熟悉的面孔或将亮相......'
    },
    {
      demo_link: 'https://movie.douban.com/subject/26816519/',
      img_link: 'http://i4.bvimg.com/617101/e72d4392218f86f2t.jpg',
      title: '逃避虽可耻但有用',
      key_word: '喜剧',
      score: 8.3,
      description: '森山实栗（新垣结衣 饰）自研究生毕业之后就一直仕途不顺，最近更是惨遭解雇。经由父亲的介绍，实栗来到了名为津崎平匡（星野源 饰）的单身男子家中，为其料理家事，就这样，二十五岁的实栗成为了一名家政妇。然而好景不长，实栗的父母决定搬离此地，这也就意味着实栗必须“离职”。实在无法接受此事的实栗决定和平匡“契约结婚”，在外装做夫妻，在内依旧是雇主和职员。就这样，这对“孤男寡女”开始了他们的同居生活......'
    }
  ];

  contentInit(demoContent) //内容初始化
  waitImgsLoad() //等待图片加载，并执行布局初始化
}());

/**
 * 内容初始化
 * @return {[type]} [description]
 */
function contentInit(content) {
  // var htmlArr = [];
  // for (var i = 0; i < content.length; i++) {
  //     htmlArr.push('<div class="grid-item">')
  //     htmlArr.push('<a class="a-img" href="'+content[i].demo_link+'">')
  //     htmlArr.push('<img src="'+content[i].img_link+'">')
  //     htmlArr.push('</a>')
  //     htmlArr.push('<h3 class="demo-title">')
  //     htmlArr.push('<a href="'+content[i].demo_link+'">'+content[i].title+'</a>')
  //     htmlArr.push('</h3>')
  //     htmlArr.push('<p>主要技术：'+content[i].core_tech+'</p>')
  //     htmlArr.push('<p>'+content[i].description)
  //     htmlArr.push('<a href="'+content[i].code_link+'">源代码 <i class="fa fa-code" aria-hidden="true"></i></a>')
  //     htmlArr.push('</p>')
  //     htmlArr.push('</div>')
  // }
  // var htmlStr = htmlArr.join('')
  var htmlStr = ''
  for (var i = 0; i < content.length; i++) {
    htmlStr += '<div class="grid-item">' + '   <a class="a-img" href="' + content[i].demo_link + '">' + '       <img src="' + content[i].img_link + '">' + '   </a>' + '   <h3 class="demo-title">' + '       <a href="' + content[i].demo_link + '">' + content[i].title + '</a>' + '   </h3>' + '   <p>关键字：' + content[i].key_word + '</p>' + '   <p>豆瓣评分：' + content[i].score + '</p>' + '   <p>剧情简介：' + content[i].description + '   </p>' + '</div>'
  }
  var grid = document.querySelector('.grid')
  grid.insertAdjacentHTML('afterbegin', htmlStr)
}

/**
 * 等待图片加载
 * @return {[type]} [description]
 */
function waitImgsLoad() {
  var imgs = document.querySelectorAll('.grid img')
  var totalImgs = imgs.length
  var count = 0
  //console.log(imgs)
  for (var i = 0; i < totalImgs; i++) {
    if (imgs[i].complete) {
      //console.log('complete');
      count++
    } else {
      imgs[i].onload = function() {
        // alert('onload')
        count++
        //console.log('onload' + count)
        if (count == totalImgs) {
          //console.log('onload---bbbbbbbb')
          initGrid()
        }
      }
    }
  }
  if (count == totalImgs) {
    //console.log('---bbbbbbbb')
    initGrid()
  }
}

/**
 * 初始化栅格布局
 * @return {[type]} [description]
 */
function initGrid() {
  var msnry = new Masonry('.grid', {
    // options
    itemSelector: '.grid-item',
    columnWidth: 250,
    isFitWidth: true,
    gutter: 20
  })
}
