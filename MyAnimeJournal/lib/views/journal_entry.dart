import 'package:flutter/material.dart';
import 'package:journal/models/anime.dart';

class JournalEntry extends StatefulWidget {
  static const routeName = 'JournalEntry';
  const JournalEntry({Key? key}) : super(key: key);

  @override
  _JournalEntryState createState() => _JournalEntryState();
}

class _JournalEntryState extends State<JournalEntry> {
  void goBack(BuildContext context) {
    Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    final Anime args = ModalRoute.of(context)?.settings.arguments as Anime;
    return Scaffold(
        appBar: AppBar(
          title: Text(args.title),
        ),
        body: Center(
            child: Padding(
          padding: const EdgeInsets.all(10),
          child: Column(children: [
            Text('Title: ${args.title}'),
            Text('Date: ${args.date}'),
            Text('Rating: ${args.rating.toString()}'),
            Text('Review: ${args.review}'),
            ElevatedButton(
                onPressed: () => goBack(context), child: const Text('Back'))
          ]),
        )));
  }
}
