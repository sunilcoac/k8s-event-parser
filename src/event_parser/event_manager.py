from kubernetes import client, config
from datetime import datetime, timedelta, timezone


class PodEventController:
    def __init__(self, model, view):
        """
        Initialize the controller with a database model and a view.
        """
        self.model = model
        self.view = view
        config.load_kube_config()  # Use config.load_incluster_config() if running inside a cluster
        self.v1 = client.CoreV1Api()

    def log_pod_events_by_type(self, namespace):
        """
        Fetch, process, and log pod events from Kubernetes without interval filtering.
        """
        print(f"Checking all pod events in namespace '{namespace}'")

        image_event_reasons = {
            "Pulling",
            "Pulled",
            "Failed",
            "InspectFailed",
            "ErrImageNeverPull",
            "BackOff",
            "Scheduled", 
            "Created"
        }

        try:
            # Fetch all events in the namespace
            events = self.v1.list_namespaced_event(namespace)
            pod_events = {}

            for event in events.items:
                # Check if the event involves a pod and matches image event reasons
                pod_name = event.involved_object.name if event.involved_object.kind == "Pod" else None
                if not pod_name or event.reason not in image_event_reasons:
                    continue

                # Classify event type
                event_type = "Warning" if event.type == "Warning" else "Normal"
                if pod_name not in pod_events:
                    pod_events[pod_name] = {"Normal": [], "Warning": []}

                event_data = {
                    "reason": event.reason,
                    "message": event.message,
                    "timestamp": event.last_timestamp or event.first_timestamp
                }
                pod_events[pod_name][event_type].append(event_data)

                # Save the event to the database
                self.model.save_event(
                    pod_name=pod_name,
                    event_type=event_type,
                    reason=event.reason,
                    message=event.message,
                    timestamp=event_data["timestamp"]
                )

            # Display the events via the view
            self.view.display_events(pod_events)

        except Exception as e:
            print(f"Error fetching events: {e}")