import 'package:flutter/material.dart';
import 'package:journal/models/anime.dart';
import 'dart:async';
import '../db/database_manager.dart';

class WelcomePage extends StatefulWidget {
  const WelcomePage(
      {Key? key,
      required this.title,
      required this.darkTheme,
      this.toggleTheme})
      : super(key: key);

  final String title;
  final bool darkTheme;
  final toggleTheme;

  @override
  State<WelcomePage> createState() => _WelcomePageState();
}

class _WelcomePageState extends State<WelcomePage> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  final databaseManager = DatabaseManager.getInstance();
  _WelcomePageState();

  @override
  void initState() {
    super.initState();
    loadJournal();
  }

  List<Anime> animes = [
    Anime(
        id: 0, title: "Naruto", review: "cool", rating: 8, date: '2022/02/02'),
    Anime(
        id: 1, title: "Bleach", review: "great", rating: 9, date: '2022/02/05')
  ];

  void loadJournal() async {
    List<Map> journalRecords = await databaseManager.journalEntries();
    setState(() {
      animes = journalRecords.map((record) {
        return Anime(
            id: record['id'],
            title: record['title'],
            review: record['body'],
            rating: record['rating'],
            date: record['date']);
      }).toList();
    });
  }

  FutureOr reloadDB(dynamic value) {
    setState(() {
      loadJournal();
    });
  }

  void _openEndDrawer() {
    _scaffoldKey.currentState!.openEndDrawer();
  }

  _addJournalEntry(BuildContext context) {
    Navigator.of(context).pushNamed('newEntry').then(reloadDB);
  }

  _viewJournalEntry(BuildContext context, anime) {
    Navigator.of(context).pushNamed('journalEntry', arguments: anime);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBar(
        title: Text(widget.title),
        actions: <Widget>[
          IconButton(
            icon: const Icon(
              Icons.settings,
              color: Colors.white,
            ),
            onPressed: () {
              _openEndDrawer();
            },
          )
        ],
      ),
      body: LayoutBuilder(builder: layoutDecider),
      endDrawer: Drawer(
          child: SwitchListTile(
              title: const Text('Dark Mode'),
              value: widget.darkTheme,
              onChanged: widget.toggleTheme)),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          _addJournalEntry(context);
        },
        tooltip: 'Add Journal Entry',
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget displayJournal(
    BuildContext context, cardSize
  ) {
    if (animes.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const <Widget>[
            Icon(Icons.book, size: 40),
            SizedBox(height: 10),
            Text('Welcome'),
            Text('Click to add an AnimeList entry')
          ],
        ),
      );
    } else {
      return buildList(context, cardSize);
    }
  }

  Widget layoutDecider(BuildContext context, BoxConstraints constraints) {
    return constraints.maxWidth < 500
        ?  displayJournal(context, smallView)
        :  displayJournal(context, largeView);
  }

  Widget buildList(BuildContext context, cardSize) {
    return ListView.builder(
        itemCount: animes.length,
        itemBuilder: (context, index) {
          return buildCard(context, index, cardSize);
        });
  }

  Widget buildCard(BuildContext context, index, cardSize) {
    return GestureDetector(
      child: cardSize(index),
      onTap: () {
        _viewJournalEntry(context, animes[index]);
      });
  }

  Widget smallView(index){
    return Card(
      child: ListTile(
        title: Text(animes[index].title),
        subtitle: Text(animes[index].date),
      ));
  }

  Widget largeView(index){
    return Card(
      child: Row(
        children: <Widget>[
          Expanded(
            child: Align(
              alignment: Alignment.centerLeft,
                child: Column(children: <Widget>[
                  Text(animes[index].title),
                  Text(animes[index].date)
                ])
            )
          ),
          Align(
            alignment: Alignment.centerRight,
            child: Column(
              children:<Widget>[
                Text(animes[index].review)
              ]
            ) 
          )
        ]
      )
    );
  }
}
