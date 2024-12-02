class ConsoleView:
    @staticmethod
    def display_events(pod_events):
        """
        Display Kubernetes pod events in the console.
        """
        for pod_name, events in pod_events.items():
            print(f"\nPod: {pod_name}")
            print("-" * 40)

            # Display normal events
            if events["Normal"]:
                print("Normal Events:")
                for event in events["Normal"]:
                    print(f"  Reason: {event['reason']}")
                    print(f"  Message: {event['message']}")
                    print(f"  Timestamp: {event['timestamp']}")
                print()

            # Display warning events
            if events["Warning"]:
                print("Warning Events:")
                for event in events["Warning"]:
                    print(f"  Reason: {event['reason']}")
                    print(f"  Message: {event['message']}")
                    print(f"  Timestamp: {event['timestamp']}")
                print()

            print("-" * 40)
